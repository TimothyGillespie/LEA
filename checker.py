import abc
import typing as typ


class Checker(abc.ABC):

    def __init__(self, config, histories_path: str):
        """
        :param config: A config object that contains the values read from lea.conf
        :param histories_path: The path to the directory that is supposed to contain the history
        files that log the differences.
        """
        self._config = config
        self._histories_path = histories_path

    @abc.abstractmethod
    def get_interval_length_config_key(self) -> str:
        """
        :return The key string for the length of the time interval after which the update should be
        repeatingly executed.
        """
        pass

    @abc.abstractmethod
    def check(self) -> typ.Optional[typ.Any]:
        """
        Execute the update/check for changes. Logs changed data to history file.
        :raises CheckingFailedException on failed connection or unparsable data etc. Supposed to
        trigger sending an error message by the calling class if too many happen successive.
        :return None if no change occured, any object containing the diff information otherwise.
        """
        pass
