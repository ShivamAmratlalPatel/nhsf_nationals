import google_crc32c
from twilio.rest import Client


def access_secret_version(project_id='able-door-377617',
                          secret_id='django-settings', version_id=3):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum.
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        print("Data corruption detected.")
        return response
    return response.payload.data.decode('UTF-8')


env_variables = access_secret_version()

TWILIO_ACCOUNT_SID = env_variables.split('\n')[2].split('=')[1]
TWILIO_AUTH_TOKEN = env_variables.split('\n')[3].split('=')[1]


def send_message(sport, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if sport == 'football':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    elif sport == 'netball':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    elif sport == 'kho':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    elif sport == 'kabaddi':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    elif sport == 'badminton':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    elif sport == 'cricket':
        message = client.messages.create(
            body=body,
            from_='+447700164737',
            to='+447511684882'
        )
    else:
        raise ValueError('Sport not found')
    return message.sid
