def extract_organizations(backend, details, response, *args, **kwargs):
    details["presspass_organizations"] = response["organizations"]
    return details

def link_organizations_to_session(backend, details, response, *args, **kwargs):
    organizations = details["presspass_organizations"]
    session = kwargs["request"].session
    session["organizations"] = organizations
    session["authenticated"] = True
    return details