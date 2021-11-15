import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event():
    event = {
    'summary': 'Junk',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
    'dateTime': '2020-07-18T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
    },
    'end': {
    'dateTime': '2020-07-18T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
    ],
    'reminders': {
    'useDefault': False,
    'overrides': [
    {'method': 'email', 'minutes': 24 * 60},
    {'method': 'popup', 'minutes': 10},
    ],
    },
    }
    return event



def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SERVICE_ACCOUNT_FILE = 'dklabs.vivarium.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        print(calendar_list)
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    new_event = create_event()
    #event = service.events().insert(calendarId='eddy.odonnell@gmail.com', body=new_event).execute()
    #print('Event created: %s' % (event.get('htmlLink')))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')


    #events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=100, singleEvents=True,  orderBy='startTime').execute()

    events_result = service.events().list(calendarId='primary').execute()


    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    #calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    #print(calendar_list_entry)


if __name__ == '__main__':
    main()
