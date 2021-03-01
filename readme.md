# Meaning
LEA is short for "LEA non est acronymum" (Grammar might need correction; working title)

# Installation

Have git and python 3.5 installed then do:
```
git clone https://gitlab.uni-koblenz.de/tigill/lea.git

```

Edit the `conf.json.sample` as is appropriate. Please enclose the values in quotation marks like this:

```
{
	"uni-email-address": "tigill@uni-koblenz.de",
	...
}
```
Then, rename the config file to `conf.json`.

Currently it is only available with the telegram notifications. Modifications will be made in the future. This is only an MVP so far.

# Usage
```
cd lea
pip3 install -r requirements.txt
python3 lea.py
```

Enter your password. It should send an empty list "[]" now via Telegram. It will keep checking for changes and send an, yet, ugly diff. 
You can also remove an entry in the `histories/grades.json`, so that on the next update a (still ugly) diff for the deleted entry will be sent.


If you encounter any issue or have suggestion please create an issue here on gitlab. I will move this project to github soon, wenn I am no longer locked out of my GitHub Account.

Please note that your command might not be `python3` or `pip3` but rather only `python` and `pip` depending on your technology stack.

# Potential Issues

When you receive an error that no module setuptools exists then use try the following command:

```
sudo apt-get install python3-setuptools
```
