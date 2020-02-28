import abc
import typing as typ


class Checker(abc.ABC):

    # In minutes
    INTERVAL_LENGTH = 10

    def __init__(self, histories_path: str):
        """
        :param histories_path: The path to the directory that is supposed to contain the history
        files that log the differences.
        """
        self._histories_path = histories_path

    @staticmethod
    def get_interval_length() -> int:
        """
        :return: How often the update/check should happen in minutes.
        """
        return Checker.INTERVAL_LENGTH

    @abc.abstractmethod
    def check(self) -> typ.Optional[typ.Any]:
        """
        Execute the update/check for changes. Logs changed data to history file.
        :raises CheckingFailedException on failed connection or unparsable data etc. Supposed to
        trigger sending an error message by the calling class if too many happen successive.
        :return None if no change occured, any object containing the diff information otherwise.
        """
        pass
