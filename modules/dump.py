# 单个字符串碰撞
def singledump(str1: str, url: str):
    r = open(url, mode='r').readlines()
    for it in r:
        if str1 in it:
            return True
    return False
