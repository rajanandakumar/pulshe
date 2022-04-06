#! /usr/bin/python3

import logging
import sys
from datetime import datetime, timedelta
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/data/pulshe/prod/ppd')
from app import app as application
application.secret_key = b"A\xe7\xafCC\xcf\x97'G\x17\tv~\xfe$\xde,;\xc7',\xcbrJ\xc9\xdb\xa6\xe7l\x07\x9a\x9f"
application.permanent_session_lifetime = timedelta(seconds=600)

