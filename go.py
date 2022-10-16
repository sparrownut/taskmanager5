import re
import time
import traceback

import zmail

import scan_task
from moduless.mail import mail_user, mail_pass, check_mail_is_do, set_mail_is_do, check_mail_is_auth, set_mail_is_auth, \
    sendmail
from scan_task import scan_targets
from utils.output_utils import print_inf, print_suc, print_err

if __name__ == '__main__':
    server = zmail.server(mail_user, mail_pass)
    try:
        while True:
            time.sleep(1)
            print_inf('check')
            latest_mail = server.get_latest()
            l_mail_id = latest_mail['Id']
            # zmail.show(latest_mail)
            l_mail_cont = ''
            if len(latest_mail['Content_text']) >= 1:
                l_mail_cont = latest_mail['Content_text'][0]
            elif len(latest_mail['Content_html']) >= 1:
                l_mail_cont = latest_mail['Content_html'][0]
            # print(latest_mail['From'])
            f = re.findall('<(.*?)>', latest_mail['From'])
            if len(f) >= 1:
                l_mail_from = f[0]
                if not check_mail_is_do(l_mail_id):
                    set_mail_is_do(l_mail_id)
                    print_inf('接收到新邮件 %s' % l_mail_from)
                    print_inf(l_mail_cont)
                    # print(zmail.show(latest_mail))
                    if not check_mail_is_auth(l_mail_from):
                        print_inf('未验证的新邮件来源')
                        # 未验证 如果有密码就算验证成功
                        if 'lsofadmin37695382' in l_mail_cont:
                            set_mail_is_auth(l_mail_from)
                            print_suc('%s验证成功' % l_mail_from)
                            sendmail([l_mail_from], '%s已经验证成功 此后发送的邮件均会被当做扫描任务处理' % l_mail_from)
                    else:
                        # 被验证过的邮件来源
                        try:
                            # 过滤函数
                            l_mail_cont = l_mail_cont.replace('<div><!--emptysign--></div>', '')
                            l_mail_cont = l_mail_cont.replace('<div></div>', '')

                            div_s = re.findall('<div>(.*?)</div>', l_mail_cont)
                            s_list = []

                            if '\n' in str(l_mail_cont):
                                # print('n')
                                s_list = str(l_mail_cont).split('\n')
                            elif len(div_s) >= 1:
                                s_list = div_s
                            else:
                                s_list = [l_mail_cont]

                            if len(s_list) >= 20:
                                sendmail([l_mail_from], '扫描任务%s条，数据量较大，可能需要处理一段时间' % len(s_list))
                            else:
                                sendmail([l_mail_from],
                                         '扫描任务%s条 预计%s秒后处理队列完毕' % (len(s_list), len(s_list) * 3))
                            rs = scan_targets(s_list)  # 开始扫描

                            if rs != -1:
                                print_suc('扫描成功')
                                con = """
    刚刚提交的内容已经加入扫描队列
    双引擎扫描
    AWVS扫描面板: %s
    XRAY扫描结果列表: http://43.228.71.245:8000/awvs2.html
    AWVS-ID: %s
                                """ % (scan_task.url,rs)
                                sendmail([l_mail_from], con)
                            else:
                                cont = """
    刚刚提交的目标不符合规范
    正确示范:
    https://baidu.com
    https://www.baidu.com
    https://m.baidu.com
                                ...
                                """
                                sendmail([l_mail_from], cont)
                        except:
                            traceback.print_exc()
                            cont = """
    刚刚提交的目标不符合规范
    正确示范:
    https://baidu.com
    https://www.baidu.com
    https://m.baidu.com
                            ...
                            """
                            sendmail([l_mail_from], cont)

            else:
                print_inf('未知来源')
    except Exception:
        traceback.print_exc()
        print_err('未知错误')
