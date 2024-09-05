import os
from pathlib import Path
import argparse
import pandas as pd
import requests

auth_endpoint = "https://www.strava.com/oauth/token"
activites_endpoint = "https://www.strava.com/api/v3/athlete/activities"

# used to f.e set the limit of fetched activities (default - 30)
ACTIVITIES_PER_PAGE = 200
# current page number with activities
PAGE_NUMBER = 1

GET_ALL_ACTIVITIES_PARAMS = {
    'per_page': ACTIVITIES_PER_PAGE,
    'page': PAGE_NUMBER
}

def get_access_token(client_id, client_secret, refresh_token):
    # these params need to be passed to get access token for retrieving actual data
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }
    res = requests.post(auth_endpoint, data=payload)
    res.raise_for_status()  # Raises error for bad HTTP responses
    access_token = res.json().get('access_token')
    return access_token


def access_activity_data(access_token, params=None):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(activites_endpoint, headers=headers, params=params)
    response.raise_for_status()
    activity_data = response.json()
    return activity_data


def run_strava_sync(client_id, client_secret, refresh_token):
    # Define the path for the CSV file
    csv_path = Path('data', 'strava_activity_data.csv')
    # If the file exists, remove it
    if csv_path.exists():
        os.remove(csv_path)
    # Fetch the access token and data
    token = get_access_token(client_id, client_secret, refresh_token)
    data = access_activity_data(token, params=GET_ALL_ACTIVITIES_PARAMS)
    # Preprocess and save the data
    df = preprocess_data(data)
    df.to_csv(csv_path, index=False)


def preprocess_data(data):
    return pd.json_normalize(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="Strava client ID")
    parser.add_argument("client_secret", help="Strava client secret")
    parser.add_argument("refresh_token", help="Strava refresh token")
    options = parser.parse_args()

    run_strava_sync(
        options.client_id,
        options.client_secret,
        options.refresh_token,
    )

