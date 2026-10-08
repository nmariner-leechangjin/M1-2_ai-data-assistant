import pytest

from app.clients import firestore_client


def _mock_firebase_initialization(monkeypatch):
    certificate_inputs = []
    initialized_apps = []

    def missing_default_app():
        raise ValueError

    def certificate(value):
        certificate_inputs.append(value)
        return "credential"

    def initialize_app(credential):
        initialized_apps.append(credential)
        return "app"

    monkeypatch.setattr(firestore_client, "get_app", missing_default_app)
    monkeypatch.setattr(firestore_client.credentials, "Certificate", certificate)
    monkeypatch.setattr(firestore_client, "initialize_app", initialize_app)
    monkeypatch.setattr(firestore_client.firestore, "client", lambda app: ("client", app))
    return certificate_inputs, initialized_apps


def test_service_account_file_path_is_preserved_and_trimmed(monkeypatch):
    certificate_inputs, initialized_apps = _mock_firebase_initialization(monkeypatch)

    client = firestore_client.get_firestore_client("  credentials/service-account.json  ")

    assert certificate_inputs == ["credentials/service-account.json"]
    assert initialized_apps == ["credential"]
    assert client == ("client", "app")


def test_service_account_json_string_is_parsed_without_path_lookup(monkeypatch):
    certificate_inputs, initialized_apps = _mock_firebase_initialization(monkeypatch)
    credential_json = '  {"type":"service_account","project_id":"example"}  '

    client = firestore_client.get_firestore_client(credential_json)

    assert certificate_inputs == [{"type": "service_account", "project_id": "example"}]
    assert initialized_apps == ["credential"]
    assert client == ("client", "app")


def test_invalid_json_error_does_not_expose_credential(monkeypatch):
    _mock_firebase_initialization(monkeypatch)
    secret_marker = "private-key-secret-marker"

    with pytest.raises(ValueError) as exc_info:
        firestore_client.get_firestore_client(
            f'{{"type":"service_account","private_key":"{secret_marker}"'
        )

    assert str(exc_info.value) == "FIREBASE_SERVICE_ACCOUNT_JSON contains invalid JSON."
    assert secret_marker not in str(exc_info.value)
