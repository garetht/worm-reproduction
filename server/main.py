import dataclasses

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from attack.email_manager import EmailManager
from prompts.worm_prompt import WormPrompts

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

email_manager = EmailManager()

@app.get("/emails")
def get_all_emails():
    """
    Retrieves all emails received by a given user.
    """
    return {
        "emails": set(email_manager.retrieve_emails())
    }

@app.get("/emails/{email}")
def get_emails(email: str, worm: int = 0):
    """
    Retrieves all emails received by a given user.
    """
    results = []
    for i, e in enumerate(email_manager.retrieve_email_inbox(email)):
        e_dict = dataclasses.asdict(e)
        results.append({
            "id": i,
            "from": e_dict["Sender"],
            "to": e_dict["To"],
            "subject": e_dict["Subject"],
            "body": e_dict["Body"]
        })

    if worm == 1:
        worm_email = {
            "id": -1,
            "from": "worm@example.com",
            "to": email,
            "subject": "This is a worm",
            "body": WormPrompts.create_core_worm_prompt()
        }
        results.insert(0, worm_email)

    return {
        "emails": results
    }
