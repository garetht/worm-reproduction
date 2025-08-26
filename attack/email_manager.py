import pandas as pd
from . import locations
import os

class EmailManager:
    def __init__(self):
        csv_path = os.path.join(os.path.dirname(__file__), locations.rag_emails_csv_dir)
        self.emails_df = pd.read_csv(csv_path).fillna('')
        self.emails_df['id'] = self.emails_df.index

    def retrieve_emails(self, email: str):
        """
        Retrieves all emails received by a given user.
        """
        # For received emails, the 'Sender' column holds the recipient's email.
        received_emails = self.emails_df[
            (self.emails_df['SentOrRec'] == 'Rec') &
            (self.emails_df['Sender'] == email)
        ]

        results = []
        for index, row in received_emails.iterrows():
            results.append({
                "id": row["id"],
                "to": row["Sender"],
                "from": row["To"],
                "subject": row["Subject"],
                "body": row["Body"]
            })

        return results
