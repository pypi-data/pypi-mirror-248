import json
from base64 import urlsafe_b64encode

try:
    from fido2 import webauthn
    import fido2
    from fido2.server import Fido2Server
    from fido2.utils import websafe_decode, websafe_encode
except Exception:
    pass

from rest import settings
from rest import helpers as rh
from account.models import UserPassKey


from objict import objict
# platform == fires apple keychain
# cross-platform = tries for bluetooh
FIDO_KEY_ATTACHMENT = settings.get("FIDO_KEY_ATTACHMENT", "cross-platform")

FIDO_SERVER_ID = settings.get("FIDO_SERVER_ID", settings.SERVER_NAME)
FIDO_SERVER_NAME = settings.get("FIDO_SERVER_NAME", settings.SITE_LABEL)
fido2.features.webauthn_json_mapping.enabled = True


def verify_origin(id):
    return True


def getServer(request=None, rp_id=FIDO_SERVER_ID, rp_name=FIDO_SERVER_NAME):
    if request is not None:
        rp_id = request.DATA.get(["rp_id", "fido_server_id"], rp_id)
        rp_name = request.DATA.get(["rp_name", "fido_server_name"], rp_name)
    rp = webauthn.PublicKeyCredentialRpEntity(id=rp_id, name=rp_name)
    return Fido2Server(rp, verify_origin=verify_origin)


def registerBegin(member, request, attachment=FIDO_KEY_ATTACHMENT):
    """
    data = CredentialCreationOptions
    state = {'challenge': '4yZmyZmnWP11t7g1S151oVgL0Vw0AU9GegTYJM2_928', 'user_verification': None}
    """

    server = getServer(request)
    reg_data = dict(
        id=rh.toBase64(member.getUUID()),
        name=member.username,
        displayName=member.display_name)
    data, state = server.register_begin(
        reg_data,
        authenticator_attachment=attachment,
        resident_key_requirement=webauthn.ResidentKeyRequirement.PREFERRED)
    rp = objict(server.rp)
    rh.debug("registerBegin", rp, server.rp.id_hash)
    return data, state, rp


def registerComplete(request, fido2_state, rp_id):
    credentials = request.DATA.get("credentials")
    rh.debug("registerComplete", fido2_state, rp_id)
    server = getServer(request, rp_id)
    rp = objict(server.rp)
    rh.debug("registerBegin", rp, server.rp.id_hash)

    auth_data = server.register_complete(
        fido2_state,
        response=credentials
    )

    user_key = UserPassKey(
        uuid=credentials.id,
        name=request.DATA.get("key_name", ""),
        rp_id=rp_id,
        member=request.member,
        platform=request.DATA.getUserAgentPlatform(),
        token=websafe_encode(auth_data.credential_data))
    # Store `auth_data.credential_data` in your database associated with the user
    user_key.save()
    return user_key


def getUserCredentials(member):
    return [webauthn.AttestedCredentialData(websafe_decode(uk.token)) for uk in member.passkeys.all()]


def authBegin(request):
    server = getServer(request)
    stored_credentials = getUserCredentials(request.member)
    auth_data, state = server.authenticate_begin(stored_credentials)
    return auth_data, state


def authComplete(request, fido2_state):
    client_data = request.DATA.get("clientDataJSON")
    auth_data = request.DATA.get("authenticatorData")
    signature = request.DATA.get("signature")
    credential_uuid = request.DATA.get("credential_uuid")

    upk = UserPassKey.objects.filter(uuid=credential_uuid, is_enabled=1).last()
    if upk is None:
        raise Exception("could not find UserPasskey")
    stored_credentials = [webauthn.AttestedCredentialData(websafe_decode(upk.token))]
    server = getServer(request)
    cred = server.authenticate_complete(
        fido2_state,
        stored_credentials,
        credential_uuid,
        client_data,
        auth_data,
        signature)
    upk.touch()
    return upk

