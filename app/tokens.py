from flask import jsonify, current_app as app
from app import db
from .auth import basic_auth


@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({ 'token': token })
