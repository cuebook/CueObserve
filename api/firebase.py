
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import db

def firebase_telemetry():

    cred = credentials.Certificate("/home/cuebook/Downloads/cueobserve-django-firebase-adminsdk-y66g7-1e0dd9cbd8.json")
    # firebase_admin.initialize_app(cred)
    # user = auth.get_user(uid)
    # print('Successfully fetched user data: {0}'.format(user.uid))

    firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cueobserve-django-default-rtdb.asia-southeast1.firebasedatabase.app/'    })

    # The app only has access to public data as defined in the Security Rules
    ref = db.reference('/public_resource')
    print(ref.get())
    