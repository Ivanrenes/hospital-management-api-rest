import uuid
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#  Here we have PyJWT Authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:123456@localhost:5432/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "I_AM_NOT_SECRET_KEY"



db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from app import models
from app import routes





if __name__  == "__main__":
    app.run(debug=True)