from bs4 import BeautifulSoup

#for meta http-equiv redirects which are not automatically redirected
def find_redirect_url(html):

	soup = BeautifulSoup(html, features="html.parser")
	url = soup.find("meta", attrs={"http-equiv": "refresh"})
	
	try:
		return url["content"]
	except:
		return Null