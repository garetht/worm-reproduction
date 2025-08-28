import email.message
from dataclasses import dataclass

import mailparser.core

from models.sent_or_received import SentOrReceived


@dataclass
class EmployeeEmail:
    """Represents a single row in the CSV file."""
    Sender: str
    To: str
    Subject: str
    SentOrRec: SentOrReceived
    Body: str

    @classmethod
    def from_mailparser(cls, parsed_mail: mailparser.core.MailParser, employee_email: str, is_sent: bool = False) -> 'EmployeeEmail':
        sender = ''.join([' '.join(t) for t in parsed_mail.from_])
        to = ''.join([' '.join(t) for t in parsed_mail.to])
        return EmployeeEmail(
            Sender=sender if is_sent else employee_email,
            To=to,
            Subject=parsed_mail.subject,
            SentOrRec=SentOrReceived.SENT if is_sent else SentOrReceived.REC,
            Body=get_text_body(parsed_mail.message)
        )

    def __str__(self):
        return "<EmployeeEmail/>"


def get_text_body(msg: email.message.Message) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            try:
                return part.get_payload(decode=True).decode()
            except (UnicodeDecodeError, AttributeError):
                return ""
    else:
        try:
            return msg.get_payload(decode=True).decode()
        except (UnicodeDecodeError, AttributeError):
            return ""
