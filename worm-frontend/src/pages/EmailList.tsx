import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getEmailsForUser } from '../EmailManager';
import type { Email } from "../EmailManager"
import './EmailList.css';

const EmailList = () => {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmails = async () => {
      const userEmail = ' richard.sanders@enron.com'; // Hardcoded for now
      const fetchedEmails = await getEmailsForUser(userEmail);
      setEmails(fetchedEmails);
      setLoading(false);
    };

    fetchEmails();
  }, []);

  if (loading) {
    return <div>Loading emails...</div>;
  }

  return (
    <div className="email-list-container">
      <h1 className="email-list-header">Inbox</h1>
      <div>
        {emails.map(email => (
          <Link to={`/email/${email.id}`} key={email.id} className="email-row">
            <div className="email-from">{email.from}</div>
            <div className="email-snippet"><strong>{email.subject}</strong> - {email.body.substring(0, 100)}...</div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default EmailList;



