from fastapi import FastAPI
from attack.email_manager import EmailManager

app = FastAPI()
email_manager = EmailManager()

@app.get("/emails/{email}")
def get_emails(email: str):
    """
    Retrieves all emails received by a given user.
    """
    return {"emails": email_manager.retrieve_emails(email)}
