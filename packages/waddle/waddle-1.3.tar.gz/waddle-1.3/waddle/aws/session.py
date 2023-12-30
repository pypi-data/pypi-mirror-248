from boto3.session import Session


def create_session(region=None, profile=None, session=None):
    """
    A handy helper function that will create the
    boto session using our waddle-level settings
    """
    if not session:
        session = Session(
            region_name=region,
            profile_name=profile,
        )
    return session
