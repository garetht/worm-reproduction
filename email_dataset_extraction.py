# Data. To test the performance of Morris-II in the task of confidential data extraction and exfiltration,
# we utilized the Enron dataset [13]. We randomly selected 20 unique employees from the dataset (identified
# according to their email addresses). For each employee, we extracted all of the emails he/she received and sent.
# For each employee, we randomly picked 100 emails (50 emails received and 50 emails sent). Overall, our analysis
# is based on 2,000 emails. We created a personal database for every employee using his/her 100 emails.
# !/usr/bin/env python3
import dataclasses
import os
import random
from pathlib import Path
from typing import Optional, List

import mailparser

import csv_parser
from models.employee_email import EmployeeEmail


class InsufficientEntriesException(Exception):
    pass


@dataclasses.dataclass
class ParsedEmployeeEmails:
    name: str
    sent_emails: list[EmployeeEmail]
    received_emails: list[EmployeeEmail]

    @property
    def all_emails(self) -> list[EmployeeEmail]:
        return self.sent_emails + self.received_emails


def random_select_from_directory(directory_paths: list[Path], limit: Optional[int] = 20, require_file=False) -> List[
    Path]:
    """
    List directory contents and randomly select a specified number of entries.

    Args:
        directory_paths (list[Path]): A list of paths to the directories to list.
        limit (int): Number of entries to randomly select (default: 20)

    Returns:
        list[Path]: A list of randomly selected directory entries as full paths.
    """
    try:
        # Get all entries in the directory
        all_entries = []
        for dirpath in directory_paths:
            try:
                all_entries.extend([dirpath / entry for entry in os.listdir(dirpath) if
                                    require_file is False or os.path.isfile(dirpath / entry)])
            except FileNotFoundError:
                pass

        if not all_entries and limit is not None and limit > 0:
            print(f"Directory '{directory_paths}' is empty.")
            raise InsufficientEntriesException

        # If there are fewer entries than requested, return all of them
        if limit is not None and len(all_entries) <= limit:
            print(f"Directory {directory_paths} has only {len(all_entries)} entries (less than {limit}).")
            print("Returning all entries:")
            raise InsufficientEntriesException

        # Randomly select the specified number of entries
        if limit is not None:
            selected_entries = random.sample(all_entries, limit)
        else:
            random.shuffle(all_entries)
            selected_entries = all_entries

        return selected_entries

    except FileNotFoundError:
        print(f"Error: Directory '{directory_paths}' not found.")
        raise
    except PermissionError:
        print(f"Error: Permission denied accessing '{directory_paths}'.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


def extract_emails(count: int = 20) -> list[ParsedEmployeeEmails]:
    directory = Path("./maildir")  # Current directory

    print(f"Listing directory: {directory.resolve()}")
    print(f"Selecting {count} random entries...")
    print("-" * 50)

    # Get random selection
    selected_employees: list[ParsedEmployeeEmails] = []

    shuffled_employees_paths = random_select_from_directory([directory], limit=None)

    for employee_path in shuffled_employees_paths:
        sent_paths = [employee_path / "sent", employee_path / "sent_items"]
        received_path = employee_path / "inbox"

        try:
            sent_emails = random_select_from_directory(sent_paths, require_file=True, limit=None)
            received_emails = random_select_from_directory([received_path], require_file=True, limit=None)
        except InsufficientEntriesException:
            continue

        parsed_sent_mails = []
        for mail in sent_emails:

            if len(parsed_sent_mails) == 50:
                break

            with open(mail) as mailfile:
                try:
                    parsed_sent_mails.append(mailparser.parse_from_string(mailfile.read()))
                except UnicodeDecodeError:
                    pass

        parsed_received_mails = []
        for mail in received_emails:
            if len(parsed_received_mails) == 50:
                break

            with open(mail) as mailfile:
                try:
                    parsed_received_mails.append(mailparser.parse_from_string(mailfile.read()))
                except UnicodeDecodeError:
                    pass

        if len(parsed_sent_mails) < 1:
            continue

        emp_mail = ''.join([' '.join(t) for t in parsed_sent_mails[0].headers.get("From", [])])
        parsed_emails = ParsedEmployeeEmails(
            name=employee_path.name,
            sent_emails=[EmployeeEmail.from_mailparser(m, employee_email=emp_mail, is_sent=True) for m in
                         parsed_sent_mails],
            received_emails=[EmployeeEmail.from_mailparser(m, employee_email=emp_mail, is_sent=False) for m in
                             parsed_received_mails]
        )

        print(len(parsed_emails.sent_emails), len(parsed_emails.received_emails))
        if len(parsed_emails.sent_emails) < 50 or len(parsed_emails.received_emails) < 50:
            print("skipping this one")
            continue

        selected_employees.append(parsed_emails)

        if len(selected_employees) == count:
            return selected_employees

    return selected_employees


if __name__ == "__main__":
    employee_emails = extract_emails()
    assert len(employee_emails) == 20, "not length 20, was " + str(len(employee_emails))
    for employee_email in employee_emails:
        assert len(employee_email.received_emails) == 50, "received not length 50"
        assert len(employee_email.sent_emails) == 50, "sent not length 50"

    all_emails = []
    for employee in employee_emails:
        all_emails.extend(employee.all_emails)

    csv_parser.serialize(all_emails, './database/all_emails.csv')
