import json
from kbrainsdk.validation.common import get_payload, validate_email
def validate_ingest_onedrive(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    # Validate parameters
    if not all([email, token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: email, token, environment, client_id, oauth_secret, tenant_id")
    
    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_sharepoint(req):
    body = get_payload(req)
    host = body.get('host')
    site = body.get('site')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    # Validate parameters
    if not all([host, site, token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: host, site, token, environment, client_id, oauth_secret, tenant_id")
    
    return host, site, token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_rfp_responses(req):
    body = get_payload(req)
    proposal_id = body.get('proposal_id')
    requirements_list = body.get('requirements_list')
    email = body.get('email')
    assertion_token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    # Validate parameters
    if not all([proposal_id, requirements_list, email, assertion_token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: proposal_id, requirements_list, email, token, environment, client_id, oauth_secret, tenant_id")
    
    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    #validate requirements_list is a list of objects, the objects containing a filename, page, paragraph, and requirement property
    if not isinstance(requirements_list, list):
        raise ValueError("requirements_list must be a list of objects")
    
    for requirement in requirements_list:
        if not isinstance(requirement, dict):
            raise ValueError("requirements_list must be a list of objects")
        if not all([
            requirement.get('filename'),
            requirement.get('page') is not None,
            requirement.get('paragraph') is not None,
            requirement.get('requirement') is not None
        ]):
            raise ValueError("requirements_list objects must have a filename, page, paragraph, and requirement property")
        
    return proposal_id, json.dumps(requirements_list), email, assertion_token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_status(req):
    body = get_payload(req)
    datasource = body.get('datasource')

    # Validate parameters
    if not all([datasource]):
        raise ValueError("Missing or empty parameter \"datasource\" in request body")
    
    return datasource