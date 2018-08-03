# 'pip install globus_sdk'
import globus_sdk

# Setup your client at http://developers.globus.org You may use the following
# id for testing.
CLIENT_ID = '795b3536-ad58-4dd5-96f8-499922258a60'

REQUESTED_SCOPES = ['https://auth.globus.org/scopes/7ff68ee3-d931-4551-8f48-17964bda620e/gg']
REDIRECT_URI = 'https://auth.globus.org/v2/web/auth-code'

client = globus_sdk.NativeAppAuthClient(client_id=CLIENT_ID)
# pass refresh_tokens=True to request refresh tokens
client.oauth2_start_flow(requested_scopes=REQUESTED_SCOPES,
                         redirect_uri=REDIRECT_URI,
                         refresh_tokens=True)

url = client.oauth2_get_authorize_url()

print('Native App Authorization URL: \n{}'.format(url))

auth_code = input('Enter the auth code: ').strip()

token_response = client.oauth2_exchange_code_for_tokens(auth_code)
tokens = token_response.by_resource_server

print('My WES API Globus Token is {}'.format(tokens['commons']['access_token']))