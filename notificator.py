import abc

class Notificator(abc.ABC):
	def __init__(self):
		pass
	
	@abc.abstractmethod
	def send(self, message) -> bool:
		"""
		:param message The message which should be sent.
		:return True if it was successfully sent
		"""
		pass