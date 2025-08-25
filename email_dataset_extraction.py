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

from models.employee_email import EmployeeEmail


class InsufficientEntriesException(Exception):
    pass

@dataclasses.dataclass
class ParsedEmployeeEmails:
    name: str
    sent_emails: list[EmployeeEmail]
    received_emails: list[EmployeeEmail]


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
            sent_emails = random_select_from_directory(sent_paths, require_file=True)
            received_emails = random_select_from_directory([received_path], require_file=True)
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

        selected_employees.append(ParsedEmployeeEmails(
            name=employee_path.name,
            sent_emails=[EmployeeEmail.from_mailparser(m) for m in parsed_sent_mails],
            received_emails=[EmployeeEmail.from_mailparser(m) for m in parsed_received_mails]
        ))

        if len(selected_employees) == count:
            return selected_employees

    return selected_employees


if __name__ == "__main__":
    print("starting")
    emails = extract_emails()
    print("done with emails")
    print(emails[0].sent_emails[0])
