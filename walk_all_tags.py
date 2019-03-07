import copy
import json
import time
import requests
from urllib.parse import urljoin

REQUEST_URL = 'http://35.177.113.43:80/'
ADD_SCORE_END_POINT = '/services.php?action=capturescore_new'
CHECK_BONUS_END_POINT = '/services.php?action=checkforbonuspoints_5hours'
API_KEY = "KhOSpc4cf67AkbRpq1hkq5O3LPlwU9IAtILaL27EPMlYr27zipbNCsQaeXkSeK3R"

# PLAYER_LIST = [("563", "c2FuamVldmVrdW1hcmdtYWlsY29t")]
PLAYER_LIST = [("550", "c3VzaG1hc2FuamVldg\u003d\u003d")]


def yeild_tags():
    get_tags_url = '/services.php?action=getallstreettags_new_jan'
    req_url = urljoin(REQUEST_URL, get_tags_url)
    post_data = {
        "api_key": API_KEY,
        "data": {
            "circuit_id": "1",
            "current_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "lat": "51.5366951",
            "lng":  "0.0798844",
            "location_id": "1",
            "player_id": 'c2FuamVldmVrdW1hcmdtYWlsY29t'
        }
    }
    r = requests.post(req_url, data=json.dumps(post_data))
    print("total = %s" % len(r.json()['data']['data']))
    return r.json()['data']['data']


def main(team_id, player_id):
    req_data_common = {"api_key": API_KEY,
                       "data": {
                        "player_id": player_id,
                        "team_id": team_id}
                       }
    req_data = copy.deepcopy(req_data_common)
    bonus_data = copy.deepcopy(req_data_common)
    url = urljoin(REQUEST_URL, ADD_SCORE_END_POINT)
    bonus_url = urljoin(REQUEST_URL, CHECK_BONUS_END_POINT)
    # all_tags = json.load(open('streettag.json'))
    # print("total = %s" % len(all_tags['data']['data']))
    count = 0
    total_score = 0
    for tag in yeild_tags()[:180]:

        req_data["data"]["lat"] = tag["lat"]
        req_data["data"]["lng"] = tag["lng"]
        req_data["data"]["location_id"] = tag["location_id"]
        req_data["data"]["score_points"] = tag["score"]
        req_data["data"]["qid"] = tag["qid"]
        req_data["data"]["circuit_id"] = tag["circuit_id"]
        req_data["data"]["current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # print(req_data)
        r = requests.post(url, data=json.dumps(req_data))
        print(r.text)
        total_score = total_score + int(tag["score"])
        bonus_data["data"]["circuit_id"] = tag["circuit_id"]
        bonus_data["data"]["current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        bonus_data["data"]["location_id"] = tag["location_id"]
        r = requests.post(bonus_url, data=json.dumps(bonus_data))
        print(r.text)
        #break
        time.sleep(10)

    print("you completed {} tags and {} score added".format(
        count, total_score))


if __name__ == '__main__':
    for t_id, p_id in PLAYER_LIST:
        main(t_id, p_id)
