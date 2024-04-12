from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)


drive_service = build('drive', 'v3', credentials=credentials)

# List files
response = drive_service.files().list().execute()
files = response.get('files', [])

# Find file by name
file_name = 'WhatsApp Chat with Boulder Climbing Partners.txt'
file_id = None
for file in files:
    if file['name'] == file_name:
        file_id = file['id']
        print(file_id)
        break

if file_id is None:
    print("File not found.")
import io

# Download file
file_request = drive_service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, file_request)
done = False
while not done :
    status, done = downloader.next_chunk()

# Read content
content = fh.getvalue().decode('utf-8')
print(content)
