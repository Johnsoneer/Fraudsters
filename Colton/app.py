APP_NAME = 'Fraud Detection API'
APP_DESCRIPTION = 'Determine the likelyhood of fraud'

import sys, os, time
from flask import Flask

import json




from flask import Flask, jsonify, g, request, redirect
# from flask_swagger import swagger

app = Flask(__name__)


@app.route('/', methods='GET')
def root():
    return redirect('FRAUD DETECTOR')


@app.route('/spec')
def spec():
    swag = swagger(app)
    swag['info']['version'] = "multiple"
    swag['info']['title'] = APP_NAME
    swag['info']['description'] = APP_DESCRIPTION
    return jsonify(swag)


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    diff = (time.time() - g.start_time) * 1000.0
    info = '%.4f ms <-- %s' % (diff, request.path)
    app.logger.info(info)
    return response
