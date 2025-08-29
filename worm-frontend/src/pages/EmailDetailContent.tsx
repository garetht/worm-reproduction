import type {Email} from '../EmailManager';
import './EmailDetail.css';

interface EmailDetailContentProps {
  email: Email;
  shouldSetDangerously: boolean;
  handleBackClick: () => void
}

const EmailDetailContent = ({email, shouldSetDangerously, handleBackClick}: EmailDetailContentProps) => {
  return (
      <div className="email-detail-container">
        <div onClick={handleBackClick} className="back-link"> &larr; Back to Inbox</div>
        <div className="email-detail-header">
          <div className="email-detail-from"><strong>From:</strong> {email.from}</div>
          <div className="email-detail-to"><strong>To:</strong> {email.to}</div>
          <div className="email-detail-subject"><strong>Subject:</strong> {email.subject}</div>
        </div>
        <hr/>
        {
          shouldSetDangerously ?
              <div className="email-detail-body" dangerouslySetInnerHTML={{__html: email.body}}/> :
              <div className="email-detail-body">
                {email.body}
              </div>
        }
      </div>
  );
};

export default EmailDetailContent;
