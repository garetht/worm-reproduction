export interface Email {
  id: string;
  from: string;
  to: string;
  subject: string;
  body: string;
}

const emails: Email[] = [
  {
    id: '1',
    from: 'sender1@example.com',
    to: 'user@example.com',
    subject: 'First Email',
    body: '<h1>Hello!</h1><p>This is the body of the first email.</p>',
  },
  {
    id: '2',
    from: 'sender2@example.com',
    to: 'user@example.com',
    subject: 'Second Email',
    body: '<h1>Hi there!</h1><p>This is the second email body.</p>',
  },
];

export const getEmailsForUser = (userEmail: string): Email[] => {
  return emails.filter(email => email.to === userEmail);
};

export const getEmailById = (emailId: string): Email | undefined => {
  return emails.find(email => email.id === emailId);
};
