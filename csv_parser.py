import csv
import sys
from typing import List

from models.employee_email import EmployeeEmail
from models.sent_or_received import SentOrReceived


def parse_csv(file_path: str) -> List[EmployeeEmail]:
    """
    Parses a CSV file with a header and a body column that can contain newlines.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A list of CsvRow objects.
    """
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # The fields might have leading/trailing whitespace, let's be safe
        if reader.fieldnames:
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
        
        for row in reader:
            try:
                sent_or_rec_enum = SentOrReceived(row['SentOrRec'])
                data.append(EmployeeEmail(
                    Sender=row['Sender'],
                    SentOrRec=sent_or_rec_enum,
                    Body=row['Body']
                ))
            except ValueError:
                print(f"Warning: Skipping row with invalid SentOrRec value: {row['SentOrRec']}", file=sys.stderr)
    return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python csv_parser.py <path_to_csv_file>")
        sys.exit(1)

    file_path: str = sys.argv[1]
    try:
        parsed_data: List[EmployeeEmail] = parse_csv(file_path)
        for row in parsed_data:
            print(row)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
