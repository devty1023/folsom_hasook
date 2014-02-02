import _config as cf
import requests
import dropbox

def wp_token():
    print cf.WP_AUTHORIZE_URL + '?client_id=' + cf.WP_CLIENT_ID + '&redirect_uri=' + \
        cf.WP_REDIRECT_URI + '&response_type=code'

    payload = {
        'client_id': cf.WP_CLIENT_ID,
        'redirect_uri': cf.WP_REDIRECT_URI,
        'client_secret': cf.WP_CLIENT_SECRET,
        'code': cf.WP_CODE,
        'grant_type': 'authorization_code'
    }

    # make post request to get permant auth token
    r = requests.post('https://public-api.wordpress.com/oauth2/token', data=payload)
    print r.text

def dp_token():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(cf.DP_APP_KEY, cf.DP_APP_SECRET)
    authorize_url = flow.start()

    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    access_token, user_id = flow.finish(code)

    print access_token, user_id

if __name__ == '__main__':
    dp_token()

