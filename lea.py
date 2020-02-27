import getpass, requests
from bs4 import BeautifulSoup
from redirect_handler import find_redirect_url


email = input("Enter your email: ")

# Can this be read out when running? Maybe split the password into different variables so they don't lie in one tracable register? Or a reversible encryption technique?
password = getpass.getpass("Enter your password: ")


session = requests.Session()

# Maybe implement this later, for now it is using the direct link. But it could be less reliable.
"""
klips_website = "https://klips.uni-koblenz.de"
response = session.get(klips_website)
if(response.status_code != 200):
	print("Did not receive the expected 200")

redirect_url = find_redirect_url(response.text)
try:
	redirect_url = redirect_url.split("=")[1]
except:
	print("Error")
	exit()

if redirect_url is None:
	print("Could not find the expected KLIPS redirect. Cannot continue.")
	exit()
	
redirect_url = klips_website + redirect_url
"""

redirect_url = "https://klips.uni-koblenz.de/qisserver/rds?state=user&type=0"

response = session.get(redirect_url)

soup = BeautifulSoup(response.text, features="html.parser")

login_form = soup.find("form")

if login_form is None:
	print("Could not find the log in form. Cannot continue.")
	exit()

# Making sure it is the correct form
if login_form.find("button", type="submit", value="Anmelden") is None:
	print("The correct log in form could not be found. Cannot continue.")
	
try:
	form_link = login_form["action"]
except:
	print("Could not find the form link.")
	exit()
	
payload = {
	# Yes, this naming convention is odd but not mine.
	"asdf": email,
	"fdsa": password,
	"anmart": "student"
}

response = session.post(form_link, data = payload)
soup = BeautifulSoup(response.text, features="html.parser")
link_tag = soup.find("a", text="Prüfungsverwaltung")
if link_tag is None:
	print("The login apparently has not worked")
	exit()

try:
	link = link_tag["href"]
except:
	print("Something went wrong")
	exit()

response = session.get(link)
soup = BeautifulSoup(response.text, features="html.parser")
link_tag = soup.find("a", text="Notenspiegel")
if link_tag is None:
	print("Something wen't wrong.")
	exit()

try:
	link = link_tag["href"]
except:
	print("Something went wrong")
	exit()

response = session.get(link)
	
print(response.text)