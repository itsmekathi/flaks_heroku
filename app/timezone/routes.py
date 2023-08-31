from flask import request, session
from app.models import Post

from . import timezone

@timezone.route('', methods=['POST'])
def set_timezone():
    '''Get timezone from the browser and store it in the session object.'''
    timezone = request.data.decode('utf-8')
    session['timezone'] = timezone
    return ""