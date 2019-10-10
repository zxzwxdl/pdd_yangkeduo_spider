import requests
from lxml import etree
import json
import urllib.parse
from antiContent_Js import js
import execjs

def getabuyunProxy():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H258SLK397"
    proxyPass = "80415F775"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

def get_next_msg(html):
    # with open('pdd.txt', 'r', encoding='utf-8') as f:
    #     html = f.read()
    parse_html = etree.HTML(html)

    data = json.loads(parse_html.xpath('//script[@id="__NEXT_DATA__"]/text()')[0])
    req_params, flip = data['props']['pageProps']['data']['ssrListData']['loadSearchResultTracking']['req_params'], \
                       data['props']['pageProps']['data']['ssrListData']['flip']
    req_params = dict(json.loads(req_params), **{"flip": flip})
    return req_params


def get_anticontent(q):
    # .encode('gbk').encode('gbk','ignore')
    ctx = execjs.compile(js)
    anti_content = ctx.call('result', q)
    return anti_content


def get_json_msg(session, req_params):
    url = "http://mobile.yangkeduo.com/proxy/api/search"
    headers = {
        'Host': 'mobile.yangkeduo.com',
        'Connection': 'keep-alive',
        'AccessToken': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        'VerifyAuthToken': 'oUa4c7ABPA_2S-6i_70a6w',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'http://mobile.yangkeduo.com/search_result.html?search_key=' + urllib.parse.quote(req_params['q']),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'api_uid=rBUoFl0B72BSXB6ppHvaAg==',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    }
    flip_temp = ''
    for page in range(2, 5):
        anti_content = get_anticontent(headers['Referer'])
        params = dict(req_params, **{"anti_content": anti_content, "pdduid": ""})
        params['page'] = page
        if page != 2:
            params['flip'] = flip_temp
        res = session.get(url, headers=headers, params=params)
        # print(res.text)
        flip_temp = res.json()['flip']
        with open('res_json.json', 'a', encoding='GBK') as f:
            f.write(res.text)
            f.write('\n\n')


def get_data():
    session = requests.session()
    url = "http://mobile.yangkeduo.com/search_result.html?search_key=学生文具用品笔"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'mobile.yangkeduo.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    res = session.get(url, headers=headers)
    req_params = get_next_msg(res.text)
    # print(req_params)
    get_json_msg(session, req_params)


if __name__ == '__main__':
    q='http://mobile.yangkeduo.com/search_result.html?search_key=' + urllib.parse.quote('学生文具用品笔'),
    # ctx = get_anticontent(q)
    get_data()
