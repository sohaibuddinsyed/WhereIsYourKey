import json
import rsa

from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature import pss
from Crypto.Hash import SHA256
import binascii

from django.http import JsonResponse, HttpRequest
from homepage.response import JsonResponseBadRequest
from django.views.decorators.http import require_http_methods
from homepage.services import CredentialService
from homepage.logging import logger
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def credential_disable(request, credential_id):
    credential_service = CredentialService()
    body_json: dict = json.loads(request.body)
    try:
        credential = credential_service.retrieve_credential_by_id(credential_id=credential_id)
        message = json.dumps(body_json["data"]).encode()
        signature = body_json["signature"]
        signature_bytes = bytes.fromhex(signature)

        publicKey = RSA.import_key("\n".join(credential.backup_server_key))
        verifier = PKCS115_SigScheme(publicKey)
        print("Signature-rec:", signature)

        result = verifier.verify(SHA256.new(message), signature_bytes)
        response = body_json["data"]

        user_key_status = response["userKeyStatus"]
        backup_key_status = response["backupKeyStatus"]

        credential_service.update_credential_status(
            credential_id=credential_id,
            user_key_status=user_key_status,
            backup_key_status=backup_key_status,
        )
    except Exception as err:
        print(str(err))
        return JsonResponseBadRequest({"error": str(err)})

    return JsonResponse({"Disabled": True})
