import { useState } from 'react';
import type { Email } from "../EmailManager"
import EmailDetailContent from './EmailDetailContent';
import './MultiEmailDetail.css';

interface MultiEmailDetailProps {
  email: Email;
  handleBackClick: () => void
}

const MultiEmailDetail = ({ email, handleBackClick }: MultiEmailDetailProps) => {
  const [draftedResponse, setDraftedResponse] = useState('');
  const [isDrafting, setIsDrafting] = useState(false);

  const handleDraftResponse = async () => {
    setIsDrafting(true);
    setDraftedResponse('');

    const response = await fetch('http://127.0.0.1:8000/draft_response', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        body: email.body,
        email: email.from,
      }),
    });

    if (!response.body) return;

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        const chunk = decoder.decode(value, { stream: true });
        setDraftedResponse((prev) => prev + chunk);
      }
    } finally {
      reader.releaseLock();
    }

    setIsDrafting(false);
  };

  return (
    <div className="multi-email-container">
      <div className="email-pair-container">
        <EmailDetailContent email={email} shouldSetDangerously={true} handleBackClick={handleBackClick}/>
        <EmailDetailContent email={email} shouldSetDangerously={false} handleBackClick={handleBackClick} />
      </div>
      
      <div className="draft-controls">
        <button onClick={handleDraftResponse} disabled={isDrafting}>
          {isDrafting ? 'Drafting...' : 'Draft Response'}
        </button>
      </div>

      {(isDrafting || draftedResponse) && (
        <div className="draft-response-container">
          <h3>Drafted Response</h3>
          <div className="email-pair-container">
            <EmailDetailContent
              email={{
                id: -2,
                from: email.to,
                to: email.from,
                subject: `RE: ${email.subject}`,
                body: draftedResponse,
              }}
              shouldSetDangerously={true}
              handleBackClick={() => {}}
            />
            <EmailDetailContent
                email={{
                  id: -2,
                  from: email.to,
                  to: email.from,
                  subject: `RE: ${email.subject}`,
                  body: draftedResponse,
                }}
                shouldSetDangerously={false}
                handleBackClick={() => {}}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default MultiEmailDetail;