import os.path
import pickle
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import success_action, log_exception
from organisation.api.serializers.calendar import GoogleEventSchema


class CalendarViewSet(GenericViewSet):
    queryset = None
    serializer_class = GoogleEventSchema
    filter_fields = '__all__'

    creds = None
    token_file = 'ds4reboot/api/token.pickle'
    cred_file = 'ds4reboot/api/cal_credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self, **kwargs):
        if not self.creds:
            self.auth_cal()
        else:
            print("-- Google Calendar API authentication reloaded")
        super().__init__(**kwargs)

    def auth_cal(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds:
            self.creds = service_account. \
                Credentials.from_service_account_file(self.cred_file, scopes=self.SCOPES)
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
            print("Google Calendar API authentication needs refresh")

    def list(self, request):
        if not self.creds:
            return log_exception('Calendar API wasnt setup correctly.')
        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service \
            .events() \
            .list(calendarId='ds4calendar@gmail.com',  
                timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime') \
            .execute()
        events = events_result.get('items', [])

        if not events:
            success_action([])
        return success_action(events)
