import os

from flask import Flask
from .health import healthstatus
from .storage.s3 import s3storage


class ConfigurationError(Exception):
    pass


S3_BUCKET = os.environ.get("S3_BUCKET")
if not S3_BUCKET:
    raise ConfigurationError("S3_BUCKET should be specified")


app = Flask(__name__)
app.register_blueprint(healthstatus)
app.register_blueprint(s3storage)
app.config["S3_BUCKET"] = S3_BUCKET

if app.config["DEBUG"]:
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@app.route("/")
def catch_all():
    return {
        "message": "Welcome to small but proud co API! Docs will be there right after we secure VC money!"
    }
