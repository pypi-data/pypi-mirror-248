# -*- coding: utf-8 -*-
# @Author  : lx

import re
from lxml import etree
from urllib import parse


def html_format(string):
    """ html去除标签 """
    dr = re.compile(r'<[^>]+>', re.S)
    not_format = dr.sub('', string)
    return not_format


def jsonp_to_json(jsonp):
    result = re.findall(r'\w+[(]{1}(.*)[)]{1}',jsonp,re.S)
    return result


def re_xpath(node,compile):
    """
    :param compile: './/span[re:match(@class, "allstar(\d0)")]/@class'
    """
    namespaces = {"re": "http://exslt.org/regular-expressions"}
    result = node.xpath(compile, namespaces=namespaces)
    return result


def url_parse(url:str):
    # 提取url中的params参数，返回item
    p = url.split('?')[1]
    item = {}
    if '&' in p:
        param = p.split('&')
        for v in param:
            k = v.split('=')
            item[k[0]] = k[1]
    else:
         k = p.split('=')
         item[k[0]] = k[1]
    return item



def change_body_resource(body,domain,types="IMAGE",mark=False):
    # 替换路径为绝对路径、添加标记
    types_item = {
        'IMAGE':'//img/@src',
        'FILE':'//a[contains(@href, ".pdf")]/@href',
        'VIDEO':'//a[contains(@href, ".mp4") or contains(@href, ".avi") or contains(@href, ".mkv")]/@href',
        'AUDIO':'//a[contains(@href, ".mp3") or contains(@href, ".wav")]/@href',
    }
    body = body.replace(' data-src=',' src=')
    doc = etree.HTML(body)
    label = 1
    for img in doc.xpath(types_item[types]):
        if img.startswith('data:image'):
            continue
        if not img.startswith('http'):
            p_img = parse.urljoin(domain,img)
            if not p_img.startswith('http'):
                p_img = domain+p_img
        else:
            p_img = img
        if '?' in p_img:
            # parse &amp;
            p_img = p_img.split('?')[0]
            img = img.split('?')[0]
        body = body.replace(img,p_img)
        # parse mark
        if mark:
            label_text = ''.join(re.findall(p_img+".*?\">",body,re.S))
            body = body.replace(label_text,label_text+"\n{%s:%s}"%(types,label))
            label+=1
    return body
