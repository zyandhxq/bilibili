import requests
import execjs
import time
import re
import hashlib
import uuid
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def get_buvid3_b_nut(url):
    response = requests.get(url=url, headers=headers)
    result = response.cookies.get_dict()
    return result['buvid3'], result['b_nut']
    # print(result['buvid3'], result['b_nut'])


def get_id(url):
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    page_text = response.text
    c = re.search(r'"cid":(.*?),', page_text)
    a = re.search(r'"aid":(.*?),', page_text)
    b = re.search(r'"bvid":(.*?),', page_text)
    s = re.search(r'"spmId":(.*?),', page_text)
    v = re.search(r'"viewseo":(.*?)}', page_text)
    cid = c.group(1)
    aid = a.group(1)
    bvid = b.group(1)
    spmid = s.group(1)
    viewseo = v.group(1)
    return aid, cid, bvid, spmid, viewseo


def get_w_rid():
    s = "e1be084baf3b4663b2465fca5bf1d8890ae7d656b8114fe1901717dd092b7ee9"
    t = ""
    index = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39,
             12,
             38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57,
             62,
             11, 36, 20, 34, 44, 52]
    for i in index:
        if s[i] is not None:
            t += s[i]
    t = t[0:32]
    o = str(int(time.time() * 1000))
    a = "wts=" + o + t
    result = hashlib.md5(a.encode())
    result = result.hexdigest()
    return result, o


def get_sid(aid, cid, w_rid, wts):
    url = 'https://api.bilibili.com/x/player/wbi/v2?aid={}&cid={}&w_rid={}&wts={}'.format(aid, cid, w_rid, wts)
    # wts时间戳
    # print(url)
    response = requests.get(url=url, headers=headers)
    result = response.cookies.get_dict()
    # print(result['sid'])
    return result['sid']


def get_uuid():
    node = execjs.get()
    fp = open('_uuid.js', 'r', encoding='utf-8')
    ctx = node.compile(fp.read())
    funcname = 'r()'
    uuid = ctx.eval(funcname)
    # print(uuid)
    return uuid


def get_lsid():
    e = str(int(time.time() * 1000))
    node = execjs.get()
    fp = open('b_lsid.js', 'r', encoding='utf-8')
    ctx = node.compile(fp.read())
    funcname = 'get_final_t(%s)' % e
    b_lsid = ctx.eval(funcname)
    return b_lsid


url = "https://www.bilibili.com/video/BV1BY4y1S7Gj/?t=0.0"
buvid3, b_nut = get_buvid3_b_nut(url)
_uuid = get_uuid()
b_lsid = get_lsid()
aid, cid, bvid, spmid, viewseo = get_id(url)
# print(buvid3, b_nut, aid, cid, bvid, spmid, viewseo)
w_rid, wts = get_w_rid()
sid = get_sid(aid, cid, w_rid, wts)
# print(buvid3, b_nut, b_lsid, sid)
CURRENT_PID = uuid.uuid1()
ftime = int(time.time())
stime = ftime + random.randint(100, 500)

cookie = "buvid3=%s; b_nut=%s; CURRENT_FNVAL=4048; b_lsid=%s; _uuid=%s; sid=%s; buvid_fp=35e43238a06483d34232fcc9a456222a; buvid4=F72A356A-AEC6-B707-319A-69B21302415A57814-023032713-sHvvlqC20wo4bInce2zgGA%%3D%%3D; CURRENT_PID=%s" % (
    str(buvid3), str(b_nut), str(b_lsid), str(_uuid), str(sid), str(CURRENT_PID))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'cookie': cookie,
    'referer': url,
}
print("开始播放量:", viewseo)
play_url = "https://api.bilibili.com/x/click-interface/click/web/h5"
ret = requests.post(url=play_url, headers=headers, data={
    "aid": aid,
    "cid": cid,
    "part": 1,
    "lv": 0,
    "ftime": ftime,
    "stime": stime,
    "type": 3,
    "sub_type": 0,
    "spmid": spmid,
})
print(ret.json())
aid, cid, bvid, spmid, viewseo = get_id(url)
print("刷之后的播放量:", viewseo)
