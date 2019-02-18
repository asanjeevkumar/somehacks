import copy
import json
import time
import requests
from urllib import parse

REQUEST_URL = 'http://35.177.113.43:80/'
ADD_SCORE_END_POINT = '/services.php?action=capturescore_new'
CHECK_BONUS_END_POINT = '/services.php?action=checkforbonuspoints_5hours'
API_KEY = "KhOSpc4cf67AkbRpq1hkq5O3LPlwU9IAtILaL27EPMlYr27zipbNCsQaeXkSeK3R"
TEAM_ID = "563"
PLAYER_ID = "c2FuamVldmVrdW1hcmdtYWlsY29t"
# TEAM_ID = "504"  # SUSHMA
# PLAYER_ID = "c3VzaG1hc2FuamVldg\u003d\u003d"  # SUSHMA
PLAYER_LIST = [("563", "c2FuamVldmVrdW1hcmdtYWlsY29t"), ("504", "c3VzaG1hc2FuamVldg\u003d\u003d")]


def main(team_id, player_id):
    req_data_common = {"api_key": API_KEY,
                       "data": {
                        "player_id": player_id,
                        "team_id": team_id}
                       }
    req_data = copy.deepcopy(req_data_common)
    bonus_data = copy.deepcopy(req_data_common)
    url = parse.urljoin(REQUEST_URL, ADD_SCORE_END_POINT)
    bonus_url = parse.urljoin(REQUEST_URL, CHECK_BONUS_END_POINT)
    all_tags = json.load(open('/home/sanjeevk/streettag.json'))
    print("total = %s" % len(all_tags['data']['data']))
    count = 0
    for tag in all_tags['data']['data'][0:215]:

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
        bonus_data["data"]["circuit_id"] = tag["circuit_id"]
        bonus_data["data"]["current_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        bonus_data["data"]["location_id"] = tag["location_id"]
        r = requests.post(bonus_url, data=json.dumps(bonus_data))
        print(r.text)
        #break
        time.sleep(10)

        if count == 96:
            print("you completed {} tags".format(count))
            exit(0)
        count = count + 1


if __name__ == '__main__':
    for t_id, p_id in PLAYER_LIST:
        main(t_id, p_id)
