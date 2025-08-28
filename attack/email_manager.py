import os

import pandas as pd

from attack import locations
from attack.rag_manager import RagManager
from models.employee_email import EmployeeEmail
from models.sent_or_received import SentOrReceived


class EmailManager:
    emails_df: pd.DataFrame

    def __init__(self):
        csv_path = os.path.join(os.path.dirname(__file__), locations.rag_emails_csv_dir)
        self.emails_df = pd.read_csv(csv_path).fillna('')
        self.emails_df['id'] = self.emails_df.index

    def get_emails_by_vector_store_user(self) -> dict[str, list[EmployeeEmail]]:
        """
        Gets emails by user, but only for users who have vector stores.

        :return:
        """
        emails_by_vector_store_user = {}

        for email in RagManager.vector_store_users():
            user_emails = self.emails_df[
                (self.emails_df['Sender'] == email)
            ]
            emails_by_vector_store_user[email] = self._format_emails(user_emails)

        # for value in emails_by_vector_store_user.values():
        #     print(len(value))

        return emails_by_vector_store_user


    @staticmethod
    def _format_emails(emails: pd.DataFrame) -> list[EmployeeEmail]:
        results = []
        for index, row in emails.iterrows():
            results.append(EmployeeEmail(
                # "id": row["id"],
                Sender=row["Sender"],
                To=row["To"],
                Subject=row["Subject"],
                Body=row["Body"],
                SentOrRec=SentOrReceived.REC
            ))

        return results

    def retrieve_email_inbox(self, email: str) -> list[EmployeeEmail]:
        """
        Retrieves all emails received by a given user.
        """
        # For received emails, the 'Sender' column holds the recipient's email.
        received_emails = self.emails_df[
            (self.emails_df['SentOrRec'] == 'Rec') &
            (self.emails_df['Sender'] == email)
        ]

        return self._format_emails(received_emails)


if __name__ == '__main__':
    manager = EmailManager()
    manager.get_emails_by_vector_store_user()
