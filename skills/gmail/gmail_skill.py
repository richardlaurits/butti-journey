from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    
    # Token sparas efter första auth
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Om inga credentials eller expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/richard-laurits/gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Spara token
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def check_unread_emails():
    """Check for unread important emails"""
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId='me',
        q='is:unread label:important',
        maxResults=5
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return "Inga viktiga olästa emails!"
    
    email_list = []
    for msg in messages:
        message = service.users().messages().get(
            userId='me', 
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject']
        ).execute()
        
        headers = message['payload']['headers']
        from_header = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        
        email_list.append(f"Från: {from_header}\nÄmne: {subject}")
    
    return "\n\n".join(email_list)

def search_emails(query, max_results=20):
    """Search emails by query string"""
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return f"Inga mejl hittades för: {query}"
    
    email_list = []
    for msg in messages:
        message = service.users().messages().get(
            userId='me', 
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        
        headers = message['payload']['headers']
        from_header = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
        
        email_list.append(f"Datum: {date}\nFrån: {from_header}\nÄmne: {subject}")
    
    return "\n\n".join(email_list)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Om argument ges, använd dem som sökfråga
        query = ' '.join(sys.argv[1:])
        print(search_emails(query))
    else:
        print(check_unread_emails())
# OpenClaw skill registration
SKILL_INFO = {
    "name": "gmail_checker",
    "description": "Check unread important emails from Gmail",
    "functions": ["check_unread_emails"]
}
