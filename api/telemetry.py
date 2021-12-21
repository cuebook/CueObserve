import requests
import secrets
import string
import uuid
import os

uuidOne = uuid.uuid1()
uniequeuid = str(uuidOne).split("-")[4]

def track_event(category, action, label=None, value=0):
    try:
        # make a UUID based on the host address and current time
        uuidOne = uuid.uuid1()
        uniequeuid = str(uuidOne).split("-")[4]
    except Exception as ex:
        # To generate a random string of length 8
        uniequeuid = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))
    GA_TRACKING_ID=os.environ.get('GA_TRACKING_ID',"UA-215749507-1")


    data = {
        'v': '1',  # API Version.
        'tid': GA_TRACKING_ID,  # Tracking ID / Property ID.
        # Anonymous Client Identifier. Ideally, this should be a UUID that
        # is associated with particular user, device, or browser instance.
        'cid': uniequeuid,
        't': 'event',  # Event hit type.
        'ec': category,  # Event category.
        'ea': action,  # Event action.
        'el': label,  # Event label.
        'ev': value,  # Event value, must be an integer
        'ua': ''
    }

    response = requests.post(
        'https://www.google-analytics.com/collect', data=data)

    # If the request fails, this will raise a RequestException. Depending
    # on your application's needs, this may be a non-error and can be caught
    # by the caller.
    response.raise_for_status()

track_event(category="User "+uniequeuid, action="server-initialized" )