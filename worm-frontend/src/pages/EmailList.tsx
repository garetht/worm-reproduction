import {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import type {Email} from "../EmailManager"
import {getEmailsForUser} from '../EmailManager';
import './EmailList.css';

const EmailList = () => {
  const userEmail = ' richard.sanders@enron.com'; // Hardcoded for now
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmails = async () => {
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
        <h1 className="email-list-header">{userEmail}'s Inbox</h1>
        <div>
          {emails.map(email => (
              <Link to={`/email/${email.id}`} key={email.id} className="email-row">
                <div className="email-snippet">
                  <div className="email-subject">
                    {email.subject.substring(0, 35)}...
                  </div>
                  <div className="email-body-preview">
                    {email.body.substring(0, 100)}...
                  </div>
                </div>
              </Link>
          ))}
        </div>
      </div>
  );
};

export default EmailList;



