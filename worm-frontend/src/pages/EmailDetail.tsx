import { useParams, Link } from 'react-router-dom';
import { getEmailById, Email } from '../EmailManager';
import './EmailDetail.css';

const EmailDetail = () => {
  const { id } = useParams<{ id: string }>();
  const email: Email | undefined = getEmailById(id!);

  if (!email) {
    return <div>Email not found</div>;
  }

  return (
    <div className="email-detail-container">
      <Link to="/" className="back-link"> &larr; Back to Inbox</Link>
      <div className="email-detail-header">
        <div className="email-detail-from"><strong>From:</strong> {email.from}</div>
        <div className="email-detail-to"><strong>To:</strong> {email.to}</div>
      </div>
      <hr/>
      <div className="email-detail-body" dangerouslySetInnerHTML={{ __html: email.body }} />
    </div>
  );
};

export default EmailDetail;
