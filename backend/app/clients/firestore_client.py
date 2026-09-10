import json
from pathlib import Path
from firebase_admin import credentials, firestore, get_app, initialize_app
def get_firestore_client(service_account_json: str):
    try: app = get_app()
    except ValueError:
        path = Path(service_account_json)
        credential = credentials.Certificate(str(path)) if path.is_file() else credentials.Certificate(json.loads(service_account_json))
        app = initialize_app(credential)
    return firestore.client(app)
