import email.message
from dataclasses import dataclass

import mailparser.core

from models.sent_or_received import SentOrReceived


@dataclass
class EmployeeEmail:
    """Represents a single row in the CSV file."""
    Sender: str
    SentOrRec: SentOrReceived
    Body: str

    @classmethod
    def from_mailparser(cls, parsed_mail: mailparser.core.MailParser, is_sent: bool = False) -> 'EmployeeEmail':
        return EmployeeEmail(
            Sender=''.join([' '.join(t) for t in parsed_mail.headers.get("From", [])]),
            SentOrRec=SentOrReceived.SENT if is_sent else SentOrReceived.REC,
            Body=get_text_body(parsed_mail.message)
        )


def get_text_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
