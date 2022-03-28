from flask import Flask
from flask_restful import Resource, Api
from db.db import init_db

app = Flask(__name__)
db = init_db(app)
api = Api(app)

from resources import *

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
