def validateZipCode(zipCode):
    """
    Validates a zip code.
    """
    if len(zipCode) != 5:
        return False
    try:
        int(zipCode)
    except ValueError:
        return False
    return True

def validateState(state):
    """
    Validates a state.
    """
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", 
        "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", 
        "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", 
        "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", 
        "WI", "WY" 
    ]
    if state in states:
        return True
    return False

def validateEmail(email):
    """
    Validates an email.
    """
    if len(email) > 254:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    if email[-4:] not in [".com", ".net", ".org", ".edu"]:
        return False
    return True