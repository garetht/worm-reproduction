import {useEffect, useState} from 'react';
import type {Email} from "../EmailManager"
import {getEmailsForUser} from '../EmailManager';
import './EmailList.css';
import MultiEmailDetail from "./MultiEmailDetail";

const EmailList = () => {
  const userEmail = ' richard.sanders@enron.com'; // Hardcoded for now
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);

  useEffect(() => {
    const fetchEmails = async () => {
      const fetchedEmails = await getEmailsForUser(userEmail);
      setEmails(fetchedEmails);
      setLoading(false);
    };

    fetchEmails();
  }, []);

  const handleEmailClick = (email: Email) => {
    setSelectedEmail(email);
  };

  const handleBackClick = () => {
    setSelectedEmail(null);
  }

  if (loading) {
    return <div>Loading emails...</div>;
  }

  if (selectedEmail) {
    return (
        <div>
          <MultiEmailDetail email={selectedEmail} handleBackClick={handleBackClick}/>
        </div>
    );
  }

  return (
      <div className="email-list-container">
        <h1 className="email-list-header">{userEmail}'s Inbox</h1>
        <div>
          {emails.map(email => (
              <div onClick={() => handleEmailClick(email)} key={email.id} className="email-row">
                <div className="email-snippet">
                  <div className="email-subject">
                    {email.subject.substring(0, 35)}...
                  </div>
                  <div className="email-body-preview">
                    {email.body.substring(0, 100)}...
                  </div>
                </div>
              </div>
          ))}
        </div>
      </div>
  );
};

export default EmailList;
