import json
import requests
import time

from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from homepage.services.credential import CredentialService

from homepage.services.registration import RegistrationService
from homepage.forms import RegistrationResponseForm
from homepage.response import JsonResponseBadRequest
from homepage.logging import logger


@csrf_exempt
def registration_verification(request: HttpRequest) -> JsonResponse:
    """
    Verify the response from a WebAuthn registration ceremony

    """
    start_time = time.time()
    body_json: dict = json.loads(request.body)

    response_form = RegistrationResponseForm(body_json)

    if not response_form.is_valid():
        return JsonResponseBadRequest(dict(response_form.errors.items()))

    form_data = response_form.cleaned_data
    username: str = form_data["username"]
    metadata: dict = form_data["metadata"]
    webauthn_response: dict = form_data["response"]

    registration_service = RegistrationService()

    try:
        verification = registration_service.verify_registration_response(
            username=username,
            response=webauthn_response,
        )

        transports: list = webauthn_response.get("transports", [])
        extensions: dict = webauthn_response.get("clientExtensionResults", {})
        ext_cred_props: dict = extensions.get("credProps", {})
        is_discoverable_credential: bool = ext_cred_props.get("rk", False)

        # Registering to key management server
        alive_response = requests.get("http://" + metadata["backupUrl"] + "/alive")

        if alive_response.status_code != 200:
            raise Exception("Backup server is down")

        backup_register_object = {
            "userID": metadata["userId"],
            "keyID": webauthn_response.get("id", ""),
            "domainName": "django:8000"
            # "domainName": settings.RP_ID
        }

        backup_register_response = requests.post(
            "http://" + metadata["backupUrl"] + "/registerKey", json=backup_register_object
        )

        if backup_register_response.status_code != 200:
            raise Exception("Backup key not registered with backup url")

        backup_object: dict = json.loads(backup_register_response.content)
        # logger.info(backup_object)
        backup_object = {
            "backupUrl": metadata["backupUrl"],
            "backupUserKey": backup_object["BackupPublicKeyUser"],
            "backupServerKey": backup_object["BackupPublicKeyServer"],
        }

        # Store credential for later
        credential_service = CredentialService()
        credential_service.store_credential(
            username=username,
            verification=verification,
            metadata=backup_object,
            transports=transports,
            is_discoverable_credential=is_discoverable_credential,
        )
    except Exception as err:
        return JsonResponseBadRequest({"error": str(err)})

    print("--- %s seconds ---" % (time.time() - start_time))
    return JsonResponse({"verified": True})
