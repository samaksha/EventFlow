
from google_auth_oauthlib.flow import Flow

from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from datetime import datetime, timedelta
import json

SCOPES=['https://www.googleapis.com/auth/calendar']


def GoogleCalendarRedirectView(request):
    """Callback view for Google OAuth2 GoogleCalendarInitView."""
    state = request.session.get('google_oauth2_state')
    if state is None:
        return redirect('GoogleCalendarInitView')  # Redirect to GoogleCalendarInitView page if state is not found

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CALENDAR_API_CREDENTIALS,
        redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/',
        scopes = SCOPES,
        state=state
    )

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in session for future use
    request.session['google_credentials'] = flow.credentials.to_json()

    # Redirect to view events page
    return redirect('view_events')


def view_events(request):
    """View to display events from a Google Calendar."""
    # Get stored credentials from session
    credentials_json = request.session.get('google_credentials')
    if credentials_json:
        credentials = Credentials.from_authorized_user_info(json.loads(credentials_json), scopes = SCOPES)
        if credentials.expired:
            # Refresh credentials if expired
            credentials.refresh(Request())
            request.session['google_credentials'] = credentials.to_json()

        # Create Google Calendar API service
        service = build('calendar', 'v3', credentials=credentials)

        timemin = (datetime.today()- (timedelta(days=30))).isoformat() + 'Z'

        try:
            # Get events from primary calendar
            events_result = service.events().list(
                calendarId='primary',
                timeMin=timemin,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            return render(request, 'events.html', {'events': events})
        except Exception as e:
            print(f'Error getting events from Google Calendar: {e}')
            messages.error(request, 'Failed to retrieve events from Google Calendar.')
            return render(request, 'events.html')
    else:
        messages.error(request, 'Please log in with your Google account first.')
    return redirect('GoogleCalendarInitView')  # Redirect to GoogleCalendarInitView page if not logged in


def GoogleCalendarInitView(request):
    """View for handling user GoogleCalendarInitView."""
    flow = Flow.from_client_secrets_file(
       settings.GOOGLE_CALENDAR_API_CREDENTIALS,
        scopes = SCOPES,
        redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/'
    )
    # print(flow)
    authorization_url, state = flow.authorization_url(access_type='offline')
    print(authorization_url)
    request.session['google_oauth2_state'] = state  # Store state in session
    return redirect(authorization_url)