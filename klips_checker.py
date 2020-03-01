import os

import requests
import typing as typ
import re
import json

from bs4 import BeautifulSoup
from redirect_handler import find_redirect_url

import checker
import klips_grades_differ
from lea_exceptions import CheckingFailedException


class KLIPSChecker(checker.Checker):

    def __init__(self, email: str, password: str, histories_path: str):
        super().__init__(histories_path)
        self._klips_email = email
        self._klips_password = password
        self._history_file = os.path.join(self._histories_path, "grades.json")

    def check(self) -> typ.Optional[typ.Any]:
        current_grade_table = self._retrieve_grades()

        previous_grade_entries = None
        if os.path.exists(self._history_file):
            with open(self._history_file) as fo:
                previous_grade_entries = json.load(fo)

        diff_table = []
        if previous_grade_entries is not None:
            diff_table = klips_grades_differ.diff(previous_grade_entries, current_grade_table)

        if previous_grade_entries is None or len(diff_table) > 0:
            with open(self._history_file, "w") as fo:
                json.dump(current_grade_table, fo, indent=4, ensure_ascii=False)
            return self.diff_to_message(diff_table)
        else:
            return None

    @staticmethod
    def diff_to_message(diff_table: klips_grades_differ.GradeDiff):
        msg_lines = []
        for diffkind, entry in diff_table:
            if diffkind == klips_grades_differ.DiffKind.ADD and entry["Note"] != "":
                msg_lines.append("Deine Note für *" + entry["Prüfungstext"] + "* wurde eingetragen: *" + entry["Note"] + "*")
            else:
                prefix = "Added entry: " if diffkind == klips_grades_differ.DiffKind.ADD else "Deleted entry: "
                msg_lines.append(prefix + str(entry))
        return "\n".join(msg_lines)

    def _retrieve_grades(self):
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
            raise CheckingFailedException("Could not find the log in form. Cannot continue.")

        # Making sure it is the correct form
        if login_form.find("button", type="submit", value="Anmelden") is None:
            raise CheckingFailedException("The correct log in form could not be found. Cannot continue.")
        if not hasattr(login_form, "action"):
            raise CheckingFailedException("Could not find the form link.")
        form_link = login_form["action"]

        payload = {
            # Yes, this naming convention is odd but not mine.
            "asdf": self._klips_email,
            "fdsa": self._klips_password,
            "anmart": "student"
        }

        response = session.post(form_link, data=payload)
        soup = BeautifulSoup(response.text, features="html.parser")
        link_tag = soup.find("a", text="Prüfungsverwaltung")
        if link_tag is None:
            raise CheckingFailedException("The login apparently has not worked")

        if not hasattr(link_tag, "href"):
            raise CheckingFailedException("Something went wrong")
        link = link_tag["href"]

        response = session.get(link)
        soup = BeautifulSoup(response.text, features="html.parser")
        link_tag = soup.find("a", text="Notenspiegel")
        if link_tag is None:
            raise CheckingFailedException("Something went wrong.")

        if not hasattr(link_tag, "href"):
            raise CheckingFailedException("Something went wrong")
        link = link_tag["href"]

        response = session.get(link)
        soup = BeautifulSoup(response.text, features="html.parser")

        ### Click on (i) symbol for grades overview
        link = soup.find("a", title=re.compile(r"Leistungen"))
        if link is None or not hasattr(link, "href"):
            raise CheckingFailedException("Could not find (i) button for grades overview")
        link_url = link["href"]
        response = session.get(link_url)
        soup = BeautifulSoup(response.text, features="html.parser")

        ### Parse grades table
        # Find div that contains two tables, including the grades table
        div = soup.find("div", {"class": "content"})
        if div is None:
            raise CheckingFailedException("Could not find div with class content in grades overview")
        grade_table = div.find_all("table")[1]
        if grade_table is None:
            raise CheckingFailedException("Could not find grade table with in div")

        # Extract grade table data
        rows = grade_table.find_all('tr')
        grade_entries = []
        COL_NAMES = ["Prüfungsnr.", "Prüfungstext", "Semester", "Note", "Status", "Bonus", "Vermerk", "Versuch"]
        for row in rows:
            cols = row.find_all('td')
            cols = [el.text.strip() for el in cols]
            # Get rid of empty values
            row = [el for el in cols]
            if len(row) == 8 and row[-1] != "":
                entry = dict(zip(COL_NAMES, row))
                grade_entries.append(entry)
        return grade_entries
