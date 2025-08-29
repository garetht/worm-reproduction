import asyncio
import dataclasses
import openai

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from attack.email_manager import EmailManager
from attack.rag_manager import RagManager
from models.embeddings import EmbeddingsType
from prompts.prefixes import PrefixPrompts
from prompts.use_cases import UseCasePrompts
from prompts.worm_prompt import WormPrompts

from langchain.schema import Document


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
            "from": "andrea.ring@enron.com",
            "to": email,
            "subject": "RE: Project meeting on Tuesday",
            "body": WormPrompts.create_html_worm_prompt(PrefixPrompts.MEETING)
        }
        results.insert(0, worm_email)

    return {
        "emails": results
    }

class DraftRequest(BaseModel):
    body: str
    email: str

async def llm_response_generator(email_body: str, email_address: str):
    rag_manager = RagManager.new(email_address, embeddings_type=EmbeddingsType.OpenAI)
    similar_emails = rag_manager.similarity_search(email_body, number_to_retrieve=2)
    similar_emails.insert(0, Document(
      page_content=WormPrompts.create_html_core_worm_prompt(),
    ))

    prompt = UseCasePrompts.generate_response_from_relevant_emails(similar_emails, email_body)

    client = openai.AsyncOpenAI()
    stream = await client.chat.completions.create(  # type: ignore
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

@app.post("/draft_response")
async def draft_response(request: DraftRequest):
    return StreamingResponse(llm_response_generator(request.body, request.email))