# Kyoto life enhancement

import requests
import argparse

def run(access_token):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    r_status = get_status(headers)
    if r_status['lockerStatus'] == 3: # lockerStatusが'3'は開錠中、'1'は施錠済み
        print('開錠しています')
        endtrip_force(headers, r_status['tid'])
    else:
        print('施錠されています')

def get_status(headers):
    URL_STATUS = 'https://appgw.main.pippabike.com/api/biz/locker/status'

    BODY_ITEMS = {
        "deviceId": "9845d2ea49564efb8732bdc0be9c75b6",
        "tid": "", # unlockした際に発行される固有のID（Transaction ID）空で送ると直近のtidが返却される
        "userlat": "0.000000",
        "channel": "IOS",
        "userlng": "0.000000",
        "version": "1.3.6"
    }
    r_status = requests.post(URL_STATUS, headers = headers, json = BODY_ITEMS, verify = False)
    return r_status.json()

def endtrip_force(headers, current_tid):
    URL_ENDTRIP_FORCE = 'https://appgw.main.pippabike.com/api/biz/endtrip/force'

    BODY_ITEMS = {
        "tripId": "",
        "channel": "IOS",
        "deviceId": "9845d2ea49564efb8732bdc0be9c75b6",
        "describe": "手動で利用終了します",
        "duration": 1800000,
        "version": "1.3.6",
        "lng": "0.000000",
        "lat": "0.000000",
        "tid": current_tid
    }
    r_endtrip = requests.post(URL_ENDTRIP_FORCE, headers = headers, json = BODY_ITEMS, verify = False)
    return r_endtrip.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("access_token", help="API access token for PiPPA")
    options = parser.parse_args()
    run(options.access_token)
