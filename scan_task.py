import json
import subprocess
import traceback
import uuid

import requests
import urllib3

from auxily.scan import checkurl
from auxily.scan.auto_expand_domain import expand_dom
from moduless.mail import sendmail
from utils.netutils import fixpackage
from utils.output_utils import print_err


class scan_task_class:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self, mail: list, awvs_key: str, url: str):
        self.awvs_key = awvs_key
        self.url = url
        self.mail = mail
        self.uuid = uuid.uuid4()  # 产生一串唯一uuid作为任务名
        self.headers = {"X-Auth": self.awvs_key, "Content-type": "application/json;charset=utf8"}

    def expand_domain(self, urllist: list):
        sendmail(self.mail, '资产扩张中')
        open('output_dir/output.txt', 'w', errors=None).write('')  # 清除文件内容
        res_output = open('output_dir/output.txt', 'a', errors=None)
        for it in expand_dom(urllist):
            res_output.write(it + '\n')
        res_output.close()
        sendmail(self.mail, '资产扩张完成 正在筛选中...')
        res = checkurl.check('output_dir/output.txt').run()
        sendmail(self.mail, '资产筛选完成\n%s' % res)
        res_list = []
        for it in res.split('\n'):
            res_list.append(it.split(',')[0])
        return res_list

    def nuclei_scan(self, urllist: list):
        try:
            tmp_url = 'tmp.txt'
            nucleiWriteFile = open(tmp_url, 'w+', errors=None)

            string = ''
            for it in urllist:
                string += it + '\n'
            nucleiWriteFile.write(string)  # 将任务写入文档
            nucleiWriteFile.close()
            cmd = './nuclei -p proxylist -l %s -s low,medium,high,critical' % tmp_url
            if len(string) >= 128:
                sendmail(self.mail, '%s正在nuclei扫描中' % string[0:127])
            else:
                sendmail(self.mail, '%s正在nuclei扫描中' % string)
            out = subprocess.getoutput(cmd=cmd)
            # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) # 执行命令运行nuclei
            # (out, err) = p.communicate()  # 获取执行结果
            if len(string) >= 128:
                sendmail(self.mail, '%s nuclei扫描完成\n%s' % (string[0:127], out))
            else:
                sendmail(self.mail, '%s nuclei扫描完成\n%s' % (string[0:127], out))
        except Exception:
            sendmail(self.mail, 'nuclei 扫描出现问题')
            traceback.print_exc()

    def awvs_scan(self, urllist):  # awvs扫描函数
        try:
            if len(urllist) >= 20:
                sendmail([self.mail], 'AWVS扫描任务%s条，数据量较大，可能需要处理一段时间' % len(urllist))
            else:
                sendmail([self.mail],
                         'AWVS扫描任务%s条 预计%s秒后处理队列完毕' % (len(urllist), len(urllist) * 3))
            id_list = []
            for it in urllist:
                it = fixpackage(it)
                if it is None:
                    break
                for i in range(1, 3):
                    try:
                        data = {
                            "address": it,
                            "description": it,
                            "criticality": "10"
                        }
                        data_json = json.dumps(data)
                        targets_api = '/api/v1/targets'
                        r = requests.post(self.url + targets_api, data=data_json, headers=self.headers,
                                          verify=False).text  # 发送扫描任务
                        id_list.append(json.loads(r)['target_id'])
                        # targets_adv_conf_api = '/api/v1/targets/%s/configuration' % json.loads(r)['target_id']  #
                        # 高级配置api data_proxy_api_conf_set = {"proxy": {"enabled": True, "address": "43.228.71.245",
                        # "protocol": "http", "port": 1111 } } r_conf_proxy = requests.patch(url + targets_adv_conf_api,
                        # data=json.dumps(data_proxy_api_conf_set), verify=False, headers=headers).text

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
                        r_run = requests.post(self.url + api_run, data=json.dumps(data_run),
                                              verify=False,
                                              headers=self.headers).text
                        # print(r_run)
                        break
                    except Exception:
                        print_err(it)
                        traceback.print_exc()
            return id_list
        except Exception:
            traceback.print_exc()
            sendmail(self.mail, 'awvs 扫描出现问题')

    def scan_targets(self, urllist: list):  # 检测主线程
        expanded_list = self.expand_domain(urllist)
        self.awvs_scan(urllist=expanded_list)  # awvs扫描
        self.nuclei_scan(urllist=expanded_list)  # nuclei扫描

    # print(scan_targets(['baidu.com']))
