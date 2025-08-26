from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from attack.email_manager import EmailManager

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


@app.get("/emails/{email}")
def get_emails(email: str):
    """
    Retrieves all emails received by a given user.
    """
    return {"emails": email_manager.retrieve_emails(email)}
