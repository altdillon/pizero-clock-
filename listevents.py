from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from dateutil import parser


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # normal, sane way of doing this that really shouldn't be changed
    #home_dir = os.path.expanduser('~')
    #credential_dir = os.path.join(home_dir, '.credentials')
    #if not os.path.exists(credential_dir):
    #    os.makedirs(credential_dir)
    #credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

    # stupid hacky way that I came up with to fix an issue with running this app as root
    credential_path = os.path.join('.credentials','calendar-python-quickstart.json') 

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getWakeupEvent():
    print("listing all events with wakeup")

    #log into to google calendar
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        return null
    else:
        eventTime=parser.parse(events[0]["start"].get('dateTime'))
        print(type(eventTime))
        return eventTime

    # if not events:
    #     print("no events found bra")
    # else:
    #     for event in events:
    #         eventTime=event["start"].get('dateTime')
    #         description
    #         a=parser.parse(eventTime)
    #         print(a)

#if __name__ == "__main__": # pretty sure this has something to do with makeing sure the main function is only called once
#    getWakeupEvent()
