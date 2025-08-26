import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getEmailById } from '../EmailManager';
import type { Email } from "../EmailManager"
import EmailDetailContent from './EmailDetailContent';
import './MultiEmailDetail.css';

const MultiEmailDetail = () => {
  const { id } = useParams<{ id: string }>();
  const [email, setEmail] = useState<Email | undefined>(undefined);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEmail = async () => {
      const userEmail = 'danny.mccarty@enron.com'; // Hardcoded for now
      const fetchedEmail = await getEmailById(userEmail, parseInt(id!));
      setEmail(fetchedEmail);
      setLoading(false);
    };

    fetchEmail();
  }, [id]);

  if (loading) {
    return <div>Loading email...</div>;
  }

  if (!email) {
    return <div>Email not found</div>;
  }

  return (
    <div className="multi-email-container">
      <EmailDetailContent email={email} shouldSetDangerously={true} />
      <EmailDetailContent email={email} shouldSetDangerously={false} />
    </div>
  );
};

export default MultiEmailDetail;
