import requests

import notificator

class TelegramNotificator(notificator.Notificator):
	
	def __init__(self, api_key: str, chat_id: str):
		super().__init__()
		self.api_key = api_key
		self.chat_id = chat_id
		
	def send(self, message: str) -> bool:
		payload = {
			"chat_id": self.chat_id,
			"text": message
		}
		
		base_link = "https://api.telegram.org/bot" + self.api_key + "/sendMessage"
		
		r = requests.post(base_link, data=payload)
		
		# This one could have gone wrong. This should be fetched later.
		return True