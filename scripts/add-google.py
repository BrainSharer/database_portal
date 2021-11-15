from calendar_api.calendar_api import google_calendar_api 

m=google_calendar_api() 
m.create_event(calendar_id='primary', start='2020-06-5T15:00:00.603111+00:00', end='2020-06-5T15:00:00.603111+00:00', desc='HEYYOU!')
