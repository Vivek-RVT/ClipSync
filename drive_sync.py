import os
import pickle
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIPBOARD_FILE = os.path.expanduser("~/.clip_sync/clipboard_data.json.aes")
TOKEN_PATH = os.path.expanduser("~/.clip_sync/token.pickle")
FOLDER_ID_PATH = os.path.expanduser("~/.clip_sync/drive_folder_id.txt")

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.expanduser("~/.clip_sync/credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_or_create_folder(service):
    if os.path.exists(FOLDER_ID_PATH):
        return open(FOLDER_ID_PATH).read().strip()

    folder_metadata = {
        'name': 'ClipSync_Backups',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')

    with open(FOLDER_ID_PATH, "w") as f:
        f.write(folder_id)
    return folder_id

def upload_clipboard():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    folder_id = get_or_create_folder(service)

    file_metadata = {
        'name': f'clipboard_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.aes',
        'parents': [folder_id]
    }
    media = MediaFileUpload(CLIPBOARD_FILE, mimetype='application/octet-stream')
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"✅ Clipboard uploaded to Google Drive: {uploaded.get('id')}")

if __name__ == "__main__":
    try:
        from googleapiclient.http import MediaFileUpload
        upload_clipboard()
    except Exception as e:
        print("❌ Upload failed:", e)
