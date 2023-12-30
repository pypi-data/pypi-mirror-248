""" Contains Abstract Base Classes for user models.
You can check this to see the declarations for functions.
"""

from functools import wraps
from abc import ABCMeta, abstractmethod
from typing import ByteString
from datetime import datetime

from sqlalchemy.orm import Session

PRIVATE_KEY = "_userPrivateKey"
PUBLIC_KEY = "_userPublicKey"
BACKUP_ECC_KEY = "_backupKeys"
BACKUP_AES_KEY = "_backupAESKeys"
KEY_CREATION_YEAR = "_accountKeysCreation"

class UserError(Exception):
    """
    Exception to be raised when an error occurs in a user model.
    """

    def __init__(self, *args: object) -> None:
        self.message = args[0]
        super().__init__()

    def __str__(self) -> str:
        return self.message


def userExistRequired(func):
    """User has to be saved in order to run this function

    Arguments:
        func -- function

    Raises:
        UserError: If user is not saved

    Returns:
        inner1
    """

    @wraps(func)
    def inner1(self, *args, **kwargs):
        """Ensure user is saved

        Raises:
            UserError: If user is not saved

        Returns:
            N/A
        """
        if self.saved and self.loggedin:
            return func(self, *args, **kwargs)
        raise UserError("This user has not yet been saved or is logged out.")

    return inner1


class user(metaclass=ABCMeta):
    """Base Class for User Models.
    You can check this to see whether a method is implemented in user models.
    """

    c: Session

    @abstractmethod
    def delete(self):
        """Delete a user

        Returns:
            None
        """

    @abstractmethod
    def login(self, pwd: str, mfaToken: str = None, fido: str = None):
        """Log the user in

        Keyword Arguments:
            pwd -- Password (default: {None})

            otp -- One-Time Password (default: {None})

            fido -- Fido Token (default: {None})

        Raises:
            UserError: Password is not set

        Returns:
            Session Key, None if user is not saved
        """

    @abstractmethod
    def restoreSession(self, key: bytes):
        """Resume session from key

        Arguments:
            key -- Session Key
        """

    @abstractmethod
    def logout(self):
        """logout Logout the user and delete the current Session"""

    @abstractmethod
    def enableMFA(self):
        """The method name says it all."""

    @abstractmethod
    def disableMFA(self):
        """The method name says it all."""

    @abstractmethod
    def saveNewUser(self, name: str, pwd: str):
        """Save a new user

        Arguments:
            name -- User Name

            pwd -- Password

        Keyword Arguments:
            fido -- Fido Token (default: {None})

        Raises:
            ValueError: If user is already saved
        """

    @abstractmethod
    def getData(self, name: str) -> ByteString:
        """Get value set by setData

        Arguments:
            name -- the key

        Raises:
            AttributeError: if a value is not set

        Returns:
            The value
        """

    @abstractmethod
    def setData(self, name: str, value: any) -> None:
        """Store user data as a key-value pair

        Arguments:
            name -- key

            value -- value
        """

    @abstractmethod
    def deleteData(self, name: str) -> None:
        """Delete key-value pair set by setData

        Arguments:
            name -- The key to remove
        """

    @abstractmethod
    def decryptWithUserKey(
        self, data: ByteString, sender=None
    ) -> bytes:
        """Decrypt data with user's key

        Arguments:
            data -- Ciphertext

        Keyword Arguments:
            sender -- If applicable sender's user name (default: {None})

        Raises:
            ValueError: if decryption fails

        Returns:
            Plaintext
        """

    @abstractmethod
    def encryptWithUserKey(self, data: ByteString, otherUsers: list[str]) -> bytes:
        """Encrypt data with user's key

        Arguments:
            data -- Plaintext

        Keyword Arguments:
            otherUsers -- List of user nameswho can decrypt it  (default: {None})

        Returns:
            List of tuples of form (user name, ciphertext, salt), check: https://docs.krptn.dev/README-USER-AUTH.html#encryption.
        """

    @abstractmethod
    def generateNewKeys(self, pwd: str):
        """Regenerate Encryption keys

        Arguments:
            pwd -- Password
        """

    @abstractmethod
    def resetPWD(self, key: str, newPWD: str):
        """Reset Password

        Arguments:
            key -- Key as provided to enablePWDReset
        """

    @abstractmethod
    def reload(self):
        """Reload encryption keys. Warning: previous keys are not purged!"""

    @abstractmethod
    def enablePWDReset(self):
        """Enable Password Reset

        Arguments:
            key -- The key needed to reset
        """

    @abstractmethod
    def revokeSessions(self):
        """Revoke all Sessions for this User

        Raises:
            UserError: If the user does not exist
        """

    @abstractmethod
    def shareGet(self, name: str) -> bytes:
        """Get data set by shareSet

        Arguments:
            name -- The "name of the data"

        Raises:
            ValueError: if decryption fails

        Returns:
            Decrypted data
        """

    @abstractmethod
    def shareSet(self, name: str, data: ByteString, otherUsers: list[str]) -> None:
        """Set data readable by others

        Arguments:
            name -- The "name" of the data

            data -- The data

            otherUsers -- List of usernames who should read it
        """

    @abstractmethod
    def shareDelete(self, name: str) -> None:
        """shareDelete Delete data set by shareSet

        Arguments:
            name -- Name of the data
        """

    @abstractmethod
    def logFailure(self):
        """logFailure Log a login failure"""

    @abstractmethod
    def getLogs(self) -> list[list[datetime, bool]]:
        """getLogs Get the login logs for the user"""

    @abstractmethod
    def setUnsafe(self, name: str, data: ByteString):
        """setUnsafe

        Args:
            name (str): Data identification
            data (ByteString): data
        """

    @abstractmethod
    def getUnsafe(self, name: str):
        """setUnsafe

        Args:
            name (str): Data identification
        """

    @abstractmethod
    def deleteUnsafe(self, name: str):
        """setUnsafe

        Args:
            name (str): Data identification
        """