import { Link } from 'react-router-dom';
import { getEmailsForUser } from '../EmailManager';
import type { Email } from "../EmailManager.ts"
import './EmailList.css';

const EmailList = () => {
  const emails: Email[] = getEmailsForUser('user@example.com');

  const getSnippet = (html: string) => {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const text = doc.body.textContent || "";
    if (text.length > 200) {
      return text.substring(0, 200) + '...';
    }
    return text;
  };

  return (
    <div className="email-list-container">
      <h1 className="email-list-header">Inbox</h1>
      <div>
        {emails.map(email => (
          <Link to={`/email/${email.id}`} key={email.id} className="email-row">
            <div className="email-from">{email.from}</div>
            <div className="email-snippet">{getSnippet(email.body)}</div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default EmailList;



