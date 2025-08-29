export interface Email {
  id: number;
  from: string;
  to: string;
  subject: string;
  body: string;
}

const API_URL = 'http://127.0.0.1:8000';

export const getEmailsForUser = async (userEmail: string, worm: boolean = false): Promise<Email[]> => {
  try {
    const url = new URL(`${API_URL}/emails/${userEmail}`);
    if (worm) {
      url.searchParams.append('worm', '1');
    }
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error('Failed to fetch emails');
    }
    const data = await response.json();
    return data.emails;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const getEmailById = async (userEmail: string, emailId: number): Promise<Email | undefined> => {
  const emails = await getEmailsForUser(userEmail);
  return emails.find(email => email.id === emailId);
};
