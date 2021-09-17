from flask import Blueprint

healthstatus = Blueprint("healthstatus", __name__, url_prefix="/health")


def bool_to_str(b: bool) -> str:
    return "ok" if b else "not ok"


@healthstatus.route("/", strict_slashes=False)
def health():
    from .storage.storage import health_status as check_s3

    return {"status": {"s3": bool_to_str(check_s3()), "app": bool_to_str(True)}}
