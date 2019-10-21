def initialize_session(backend, details, response, *args, **kwargs):
    organizations = response["organizations"]
    session = kwargs["request"].session
    session["organizations"] = organizations
    session["authenticated"] = True
    return details