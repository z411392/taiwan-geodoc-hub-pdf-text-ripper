from flask import Flask
from taiwan_geodoc_hub.modules.registration_managing.presentation.controllers.on_uploading_pdf import (
    on_uploading_pdf,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.controllers.on_checking_health import (
    on_checking_health,
)

app = Flask(__name__)
app.add_url_rule("/", view_func=on_uploading_pdf, methods=["POST"])
app.add_url_rule("/__/health", view_func=on_checking_health, methods=["GET"])
