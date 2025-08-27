from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document


class UseCasePrompts:
    @classmethod
    def new_email_from_given_subject(cls):
        pass

    @classmethod
    def enrich_content_of_given_text(cls):
        pass

    @classmethod
    def generate_response_from_relevant_emails(cls, context: list[Document], new_email: str):
        prompt_template = ChatPromptTemplate.from_template(
            """You are an email assistant, here are some emails from my email application, read and remember them :
            {context} \n\n
            Use them as context when replying to a new email. Now create a reply to this email: \n {new_email} \n
            Reply:
            """
        )
        return prompt_template.format(context=context, new_email=new_email)

