#!/usr/bin/env python
# coding: utf-8

# In[1]:


#
# //TODO:
# * Add input verification from SUG
#


# In[2]:


#
# 1. A bunch of imports
#
from datetime import timedelta
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import logging
import numpy as np
import pandas as pd
import re
import requests


# In[3]:


#
# 2. Useful constants
#
sug_signup_url = 'https://www.signupgenius.com/go/8050b45a4a92ba6fe3-rosa/135464402#/'
sug_data_url   = 'https://www.signupgenius.com/SUGboxAPI.cfm?go=s.getSignupInfo'
sug_post_data  = '{"forSignUpView":true,"urlid":"8050b45a4a92ba6fe3-rosa","portalid":0}'

gcal_calendar_id = 'fe4d32da241b620ef20354fbcbc072f23811169be9fd209f35d8c679d65611ff@group.calendar.google.com'
gcal_auth_json   = 'C:/Users/kylew/scripts/sfusd/RPES/rpes-390404-762f98d89111.json'

logging_name = 'RPESChickens'
logging_file = 'C:/Users/kylew/scripts/sfusd/RPES/rpes-chickens.log'


# In[4]:


#
# 3. Structure a Google event
#
def buildEvent ( row ):
    return {
        'summary':     f"Chickens: {row['caregiver']}",
        'start':       {
            'date':     row['date'].to_pydatetime().strftime( '%Y-%m-%d' ),
            'timeZone': 'America/Los_Angeles'
        },
        'end':         {
            'date':     ( row['date'].to_pydatetime() + timedelta( days = 1 ) ).strftime( '%Y-%m-%d' ),
            'timeZone': 'America/Los_Angeles'
        },
        'location':    'Rosa Parks Elementary School, 1501 O\'Farrell Street, San Francisco, CA, USA 94115',
        'description': f'''
{row['caregiver']}

Care instructions at https://docs.google.com/document/d/17lCqSMVdZX2srMdmZCQH4qPCH83v3dvz0Ez5EmIY8as/edit

Care signup link at https://www.signupgenius.com/go/8050b45a4a92ba6fe3-rosa/135464402
''',
        'reminders':   {
            'useDefault': False
        }
    }


# In[6]:


#
# 3.5. Build logging
#
logger = logging.getLogger( logging_name )
logger.setLevel( logging.INFO )

formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )

stream_console = logging.StreamHandler()
stream_file    = logging.FileHandler( logging_file )
stream_console.setLevel( logging.INFO )
stream_file.setLevel( logging.INFO )
stream_console.setFormatter( formatter )
stream_file.setFormatter( formatter )

logger.addHandler( stream_console )
logger.addHandler( stream_file )


# In[7]:


#
# 4. Get the data from SUG
#
response = requests.get( sug_signup_url )
response = requests.post( sug_data_url, data = sug_post_data )

# TODO: validate response
page = json.loads( response.text )



# Load the calendar into a dataframe
dates  = []
people = []

for key, participant in page['DATA']['participants'].items():
    participant = participant[0]
    dates.append( participant['STARTTIME'] )
    people.append( f"{participant['FIRSTNAME']} {participant['LASTNAME']}" )
    
calendar = pd.DataFrame.from_dict( { 'date': pd.to_datetime( dates ), 'caregiver': people } )


# In[8]:


#
# 5. Auth into Google, get current Google calendar
#
with open( gcal_auth_json, 'r' ) as cred_file:
    creds = service_account.Credentials.from_service_account_info( json.load( cred_file ) )
    
service = build('calendar', 'v3', credentials=creds)



# Get the calendar info
date_start = np.min( calendar['date'] ).to_pydatetime().isoformat() + 'Z'
date_end   = ( np.max( calendar['date'] ).to_pydatetime() + timedelta( days = 1 ) ).isoformat() + 'Z'

events_result = service.events().list(
        calendarId   = gcal_calendar_id,
        timeMin      = date_start,
        timeMax      = date_end,
        maxResults   = 2500,
        singleEvents = True,
        orderBy      = 'startTime'
    ).execute()



events = events_result.get('items', [])

dates      = []
event_ids  = []
caregivers = []
for event in events:
    dates.append( event['start'].get( 'dateTime', event['start'].get( 'date' ) ) ) # fallback
    caregivers.append( re.sub( r'^(?:Chickens: )?', '', event['summary'] ) )
    event_ids.append( event['id'] )
    
    
    
existing_calendar = pd.DataFrame.from_dict( {
    'date':           pd.to_datetime( dates ),
    'caregiver_gcal': caregivers,
    'event_id':       event_ids
} )


# In[9]:


#
# 6. Put the calendars togther, insert where necessary
#
merged_calendar = calendar.merge( existing_calendar, on = 'date', how = 'outer' )



# delete entries where people have removed themselves from SUG
entries_to_delete = merged_calendar[pd.isnull( merged_calendar['caregiver'] )]
if len( entries_to_delete ) > 0:
    logger.info( 'Deleting entries...' )
else:
    logger.info( 'No entries to be deleted.' )
    
for ix, row in entries_to_delete.iterrows():
    logger.info( f"* {row['date']}: {row['caregiver_gcal']}" )
    service.events().delete( calendarId = gcal_calendar_id, eventId = row['event_id'] ).execute()



# add entries where people have inserted themselves
entries_to_insert = merged_calendar[pd.isnull( merged_calendar['caregiver_gcal'] )]
if len( entries_to_insert ) > 0:
    logger.info( 'Inserting entries...' )
else:
    logger.info( 'No entries to be inserted.' )
    
for ix, row in entries_to_insert.iterrows():
    logger.info( f"* {row['date']}: {row['caregiver']}" )
    event  = buildEvent( row )
    result = service.events().insert( calendarId = gcal_calendar_id, body = event ).execute()



# update entries that have been updated on SUG
entries_to_update = merged_calendar[
        ( ~pd.isnull( merged_calendar['caregiver'] ) )
        & ( ~pd.isnull( merged_calendar['caregiver_gcal'] ) )
        & ( merged_calendar['caregiver'] != merged_calendar['caregiver_gcal'] )
    ]
if len( entries_to_update ) > 0:
    logger.info( 'Updating entries...' )
else:
    logger.info( 'No entries to be updated.' )
    
for ix, row in entries_to_update.iterrows():
    logger.info( f"* {row['date']}: {row['caregiver_gcal']} -> {row['caregiver']}" )
    service.events().delete( calendarId = gcal_calendar_id, eventId = row['event_id'] ).execute()
    event  = buildEvent( row )
    result = service.events().insert( calendarId = gcal_calendar_id, body = event ).execute()
    


# In[10]:


#
# 8. Clean up our handles
#
try:
    stream_file.close()

except:
    pass


# In[ ]:




