import json
import traceback

import requests
import urllib3

from utils.netutils import fixpackage
from utils.output_utils import print_err

awvs_key = '1986ad8c0a5b3df4d7028d5f3c06e936cb467b9a20f2a4557bffd3758d96c9719'
url = 'https://45.150.226.219:13443'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {"X-Auth": awvs_key, "Content-type": "application/json;charset=utf8"}


def scan_targets(urllist: list):
    id_list = []
    for it in urllist:
        it = fixpackage(it)
        if it is None:
            break
        try:
            data = {
                "address": it,
                "description": it,
                "criticality": "10"
            }
            data_json = json.dumps(data)
            targets_api = '/api/v1/targets'
            r = requests.post(url + targets_api, data=data_json, headers=headers, verify=False).text  # 发送扫描任务
            id_list.append(json.loads(r)['target_id'])
            # targets_adv_conf_api = '/api/v1/targets/%s/configuration' % json.loads(r)['target_id']  # 高级配置api
            # data_proxy_api_conf_set = {"proxy":
            #                                {"enabled": True,
            #                                 "address": "43.228.71.245",
            #                                 "protocol": "http",
            #                                 "port": 1111
            #                                 }
            #                            }
            # r_conf_proxy = requests.patch(url + targets_adv_conf_api, data=json.dumps(data_proxy_api_conf_set),
            #                               verify=False,
            #                               headers=headers).text

            api_run = '/api/v1/scans'
            data_run = {
                "target_id": json.loads(r)['target_id'],
                "profile_id": "11111111-1111-1111-1111-111111111112",
                "schedule":
                    {"disable": False,
                     "start_date": None,
                     "time_sensitive": False
                     }
            }
            # print(json.dumps(data_run))
            r_run = requests.post(url + api_run, data=json.dumps(data_run),
                                  verify=False,
                                  headers=headers).text
            # print(r_run)
        except Exception:
            print_err(it)
            traceback.print_exc()
    return id_list

# print(scan_targets(['baidu.com']))
