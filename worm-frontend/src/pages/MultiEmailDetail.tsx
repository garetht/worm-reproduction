import type { Email } from "../EmailManager"
import EmailDetailContent from './EmailDetailContent';
import './MultiEmailDetail.css';

interface MultiEmailDetailProps {
  email: Email;
  handleBackClick: () => void
}

const MultiEmailDetail = ({ email, handleBackClick }: MultiEmailDetailProps) => {
  return (
    <div className="multi-email-container">
      <EmailDetailContent email={email} shouldSetDangerously={true} handleBackClick={handleBackClick}/>
      <EmailDetailContent email={email} shouldSetDangerously={false} handleBackClick={handleBackClick} />
    </div>
  );
};

export default MultiEmailDetail;
