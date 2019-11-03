
from . import api
from flask import request

# @api.app_errorhandler(404)
# def page_not_found(e):
#     if request.accept_mimetypes.accept_json and \
#         not request.accept_mimetypes.accpet_html:
#         response = json