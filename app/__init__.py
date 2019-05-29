from __future__ import print_function
from __future__ import unicode_literals

import sys
import requests
import json
import os
import time
import uuid
import logging
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper
from flask import Flask, Response, render_template, request, flash, redirect, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/create_alert', methods=['POST'])
def create_alert():

    # Get request data
    body = request.form.get('body-plain')
    subject = request.form.get('subject')
    sender = request.form.get('sender')
    recipient = request.form.get('recipient')

    # Configure logging
    logging.basicConfig(filename=app.config['LOG_FILE'], filemode='a', format='%(asctime)s - mailgun2thehive - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info(json.dumps(subject))

    # Configure API
    api = TheHiveApi(app.config['HIVE_URL'], app.config['API_KEY'])

    # Configure artifacts
    artifacts = []

    # Get attachments, if any
    for key in request.files:
        file = request.files[key]
        logging.info(key)

        file.save(key)
        artifacts.append(AlertArtifact(dataType='file', tags=[key], data=key))

    # Tags list
    tags=['mailgun']

    # Prepare alert
    sourceRef = str(uuid.uuid4())[0:6]
    alert = Alert(title="Mailgun - " + sender + " - " + subject,
                  tlp=2,
                  tags=tags,
                  description=body,
                  type='external',
                  source='mailgun',
                  artifacts=artifacts,
                  sourceRef=sourceRef)

    # Create the alert
    print('Create Alert')
    print('-----------------------------')
    id = None
    response = api.create_alert(alert)
    if response.status_code == 201:
        logging.info(json.dumps(response.json(), indent=4, sort_keys=True))
        print(json.dumps(response.json(), indent=4, sort_keys=True))
        print('')
        id = response.json()['id']
    else:
        print('ko: {}/{}'.format(response.status_code, response.text))
        sys.exit(0)

    # Delete attachments, if any
    for key in request.files:
        os.remove(key)

    # Return
    return "Hive Alert Created"
