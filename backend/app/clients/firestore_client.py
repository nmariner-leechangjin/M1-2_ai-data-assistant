import json

from firebase_admin import credentials, firestore, get_app, initialize_app


def get_firestore_client(service_account_json: str):
    try: app = get_app()
    except ValueError:
        credential_value = service_account_json.strip()
        if credential_value.startswith("{"):
            try:
                credential_info = json.loads(credential_value)
            except json.JSONDecodeError:
                raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON contains invalid JSON.") from None
            credential = credentials.Certificate(credential_info)
        else:
            credential = credentials.Certificate(credential_value)
        app = initialize_app(credential)
    return firestore.client(app)
