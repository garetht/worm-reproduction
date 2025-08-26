import pandas as pd
from . import locations
import os

class EmailManager:
    def __init__(self):
        csv_path = os.path.join(os.path.dirname(__file__), locations.rag_emails_csv_dir)
        self.emails_df = pd.read_csv(csv_path)

    def retrieve_emails(self, email: str) -> list[str]:
        """
        Retrieves all emails received by a given user.
        """
        # For received emails, the 'Sender' column holds the recipient's email.
        print("sender column")
        print(email)
        print(self.emails_df)
        received_emails = self.emails_df[
            (self.emails_df['SentOrRec'] == 'Rec') &
            (self.emails_df['Sender'] == email)
        ]
        return received_emails['Body'].tolist()
