import traceback

import requests
from netaddr import IPNetwork

from moduless.dump import singledump
from utils.netutils import fixpackage, check_ip, check_dom, check_url, check_cidr, init_headers
from utils.output_utils import print_err, print_inf, print_suc


# 从文件中获取ip信息
def geturlsfromfile(url_open: str):
    try:
        print_inf('过滤地址中')
        fop = open(url_open, encoding='utf8', mode='r')
        ip_list = []
        for it in fop:  # it 在打开的目标文件中遍历 可能有ip/域名/url
            it = fixpackage(it)
            url = []
            if check_ip(it):  # 如果是ip
                r = sethttpsuffix(it)
                if len(r) > 0:
                    for itt in r:
                        url.append(itt)
                        print_suc(itt)
            elif check_dom(it):  # 如果是域名
                r = sethttpsuffix(it)
                if len(r) > 0:
                    for itt in r:
                        url.append(itt)
                        print_suc(itt)
            elif check_url(it):  # 如果是url
                r = sethttpsuffix(it)
                if len(r) > 0:
                    for itt in r:
                        url.append(itt)
                        print_suc(itt)
            elif check_cidr(it):  # 如果是cidr
                ips = list(IPNetwork(it))  # 从cidr获取ip列表
                # print(ips)
                for ips_it in ips:
                    r = str(ips_it).replace("IPAddress(", '')
                    r = r.replace(")", '')
                    r = r.replace("'", '')
                    r = sethttpsuffix(r)
                    if len(r) > 0:
                        for itt in r:
                            url.append(itt)
                            print_suc(itt)
            else:
                print_err('无法识别%s' % it)
            for url_it in url:  # 防止cidr格式的
                ip_list.append(url_it)
        return ip_list
    except FileNotFoundError:
        print_err('没有%s文件' % url_open)
    except Exception:
        traceback.print_exc()
        print_err('错误')


# 判断是否为登陆页面
def first_judg(inp: str):
    if singledump(str1=requests.get(url=inp, headers=init_headers).text, url='dic/login_judg.dic'):
        print_inf('%s存在登录页面' % inp)
        return True
    return False


# 判断是否有验证码
def captcha_judg(inp: str):
    if singledump(str1=requests.get(url=inp, headers=init_headers).text, url='dic/captcha.dic'):
        print_inf('%s存在验证码' % inp)
        return True
    return False


# 添加协议前缀
def sethttpsuffix(url: str):
    res = []
    if 'http' not in url:
        r = tryprot(url)
        if r is not None:
            for it in r:
                res.append(it + url)
    else:
        res.append(url)
    return res


# 测试是哪种协议
def tryprot(domorip: str):
    reslist = []
    err = 2
    try:
        suf_domorip = '%s%s' % ('http://', domorip)
        requests.get(url=suf_domorip, timeout=0.5)
        reslist.append('http://')
    except Exception:
        err -= 1
    try:
        suf_domorip = '%s%s' % ('https://', domorip)
        requests.get(url=suf_domorip, timeout=0.5)
        reslist.append('https://')
    except Exception:
        err -= 1
    # 判断是否两种协议都不能访问
    if err <= 0:
        print_err('无法访问%s' % domorip)
    return reslist


#
# sethttpsuffix('baidu.com')
# print(list(IPNetwork("192.168.1.1/24")))
print(geturlsfromfile('../testfile.inp'))
