from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
import io
from googleapiclient.http import MediaIoBaseDownload

# define path variables
credentials_file_path = './credentials/credentials.json'
clientsecret_file_path = './credentials/client_secret.json'

# define API scope
SCOPE = 'https://www.googleapis.com/auth/drive'

# define store
store = file.Storage(credentials_file_path)
credentials = store.get()
# get access token
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(clientsecret_file_path, SCOPE)
    credentials = tools.run_flow(flow, store)


def get_file(file_id):
    DRIVE = discovery.build('drive', 'v3', http=credentials.authorize(Http()))
    # if you get the shareable link, the link contains this id, replace the file_id below
    #file_id = '1S4Qq3FNbrNhcGME2oJaXhgVceeSuqnjJ'
    request = DRIVE.files().get_media(fileId=file_id)
    # replace the filename and extension in the first field below
    fh = io.FileIO('matches_formatted.csv', mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
