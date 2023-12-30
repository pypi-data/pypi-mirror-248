""" Extended auth logic
"""
# pylint: disable=no-member
# pylint: disable=attribute-defined-outside-init
# pylint: disable=abstract-method
import os
from sqlalchemy import select, delete, update

from .. import factors
from ... import DBschemas, configs, base
from .bases import userExistRequired, user, UserError

FIDO_TEMP_CHALLANGE = "_tempFIDORegisterChallenge"


class MFAUser(user):
    """MFA for Krypton Users"""

    @userExistRequired
    def enablePWDReset(self) -> list[str]:
        """Enable PWD Reset

        Returns:
            The recovery codes that unlock the account
        """
        # pylint: disable=invalid-name
        PKeys = [base.genOTP() for i in range(10)]
        self.c.execute(
            delete(DBschemas.PWDReset).where(DBschemas.PWDReset.Uid == self.id)
        )
        for PKey in PKeys:
            salt = os.urandom(configs._saltLen)
            key = base.passwordHash(
                PKey, salt, configs.defaultPasswordResetArgonOps, 32
            )
            skey = base.seal(self._key, key)
            base.zeromem(key)
            row = DBschemas.PWDReset(
                Uid=self.id,
                key=skey,
                iter=configs.defaultPasswordResetArgonOps,
                salt=salt,
            )
            self.c.add(row)
            self.c.flush()
        self.c.commit()
        return PKeys

    def resetPWD(self, key: str, newPWD: str):
        assert isinstance(key, str)
        assert isinstance(newPWD, str)
        """Reset a PWD using a recovery code

        Arguments:
            key -- The recovery code

            newPWD -- The new PWD

        Raises:
            ValueError: if the reset fails
        """
        rows = (
            self.c.execute(
                select(DBschemas.PWDReset).where(DBschemas.PWDReset.Uid == self.id)
            )
            .scalars()
            .all()
        )
        reset = False
        for row in rows:
            krKey = base.passwordHash(key, row.salt, row.iter, 32)
            try:
                self._key = base.unSeal(row.key, krKey)
            except ValueError:
                continue
            base.zeromem(krKey)
            self.loggedin = True
            self.c.execute(
                delete(DBschemas.PWDReset).where(DBschemas.PWDReset.id == row.id)
            )
            self.c.flush()
            self.generateNewKeys(newPWD)
            token = self.login(newPWD)
            reset = True
            break
        if not reset:
            base.sleepOutOfGIL()
            raise ValueError("Password reset failure")
        self.c.commit()
        return token

    @userExistRequired
    def disablePWDReset(self):
        """Disbale PWD and revoke all codes"""
        self.c.execute(
            delete(DBschemas.PWDReset).where(DBschemas.PWDReset.Uid == self.id)
        )
        self.c.flush()
        self.c.commit()

    @userExistRequired
    def enableMFA(self):
        """Enable TOTP MFA

        Returns:
            base32 encoded shared secret, QR code string
        """
        secret, base32Secret, string = factors.totp.createTOTP(self.userName)
        stmt = (
            update(DBschemas.UserTable)
            .where(DBschemas.UserTable.name == self.userName)
            .values(mfa=base.seal(secret, self._key))
        )
        self.c.execute(stmt)
        self.c.flush()
        self.c.commit()
        base.zeromem(secret)
        return base32Secret, string

    @userExistRequired
    def disableMFA(self):
        """Disable TOTP based MFA"""
        stmt = (
            update(DBschemas.UserTable)
            .where(DBschemas.UserTable.name == self.userName)
            .values(mfa=b"*")
        )
        self.c.execute(stmt)
        self.c.flush()
        self.c.commit()

    @userExistRequired
    def beginFIDOSetup(self):
        """Being FIDO Registration"""
        options, challenge = factors.fido.register(self.id, self.userName)
        self.setData(FIDO_TEMP_CHALLANGE, challenge)
        return options

    @userExistRequired
    def completeFIDOSetup(self, response):
        """Finish FIDO Setup

        Arguments:
            repsonse -- The response from the client
        """
        challenge = self.getData(FIDO_TEMP_CHALLANGE)
        self.deleteData(FIDO_TEMP_CHALLANGE)
        credID, credKey = factors.fido.register_verification(response, challenge)
        self.c.execute(
            update(DBschemas.UserTable)
            .where(DBschemas.UserTable.name == self.userName)
            .values(fidoPub=credKey, fidoID=credID)
        )
        self.c.flush()
        self.c.commit()

    @userExistRequired
    def removeFIDO(self):
        """Remove the FIDO Auth from Server"""
        self.c.execute(
            update(DBschemas.UserTable)
            .where(DBschemas.UserTable.name == self.userName)
            .values(fidoPub=b"*", fidoID=b"*")
        )
        self.c.flush()
        self.c.commit()

    def getFIDOOptions(self):
        """Obtain FIDO options before Auth

        Returns:
            Fido Options as string, { "error": "No keys availble" } if FIDO is not setup
        """
        if not self.saved:
            raise UserError("This user does not exist.")
        stmt = (
            select(DBschemas.UserTable)
            .where(DBschemas.UserTable.id == self.id)
            .limit(1)
        )
        authTag: DBschemas.UserTable = self.c.scalar(stmt)
        if authTag.fidoID == b"*":
            return '{ "error": "No keys availble" }'
        options, challenge = factors.fido.authenticate(authTag.fidoID)
        self.c.execute(
            update(DBschemas.UserTable)
            .where(DBschemas.UserTable.id == self.id)
            .values(fidoChallenge=challenge)
        )
        self.c.flush()
        self.c.commit()
        return options
