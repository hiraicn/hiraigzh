# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import re
import json
import urllib,urllib2
from lxml import etree
import requests

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="7788414" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
    
    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        mstype = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        
        
        if mstype == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                replayText = u'''你好，欢迎关注。这里暂处于测试阶段，会不定期增加新功能。'''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
        
        if mstype == 'text':
            content = xml.find("Content").text#获得用户所输入的内容         
            if content == u"电台" or content == "fm" or content == "Fm" or content == "FM":
                url = 'http://m.xinli001.com/fm/'
                fmre = urllib.urlopen(url).read()
                pa1 = re.compile(r'<head>.*?<title>(.*?)-心理FM</title>',re.S)
                ts1 = re.findall(pa1,fmre)
                pa3 = re.compile(r'var broadcast_url = "(.*?)", broadcastListUrl = "/fm/items/',re.S)
                ts3 = re.findall(pa3,fmre)              
                req = urllib2.Request(ts3[0])
                response = urllib2.urlopen(req)
                redirectUrl = response.geturl()
                musicTitle = ts1[0]
                musicDes =  ''
                musicURL = redirectUrl
                HQURL = 'http://m.xinli001.com/fm/'
                return self.render.reply_sound(fromUser,toUser,musicTitle,musicDes,musicURL,HQURL)
            
            elif content == u'灌篮高手':
                title1 = '片中神曲集合'
                description1 = '燃！'
                xc = 'http://www.bilibili.com/video/av49630/'
                pic = 'http://i1.3conline.com/images/piclib/201305/29/batch/1/177167/1369797592125388tvgwker.jpg'
                return self.render.reply_pic(fromUser,toUser,title1,description1,pic,xc)
            

            else:
                key = 'fd1e5e6c82f446759c6017268151f434'
            	api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='  
            	info = content.encode('UTF-8') 
            	url = api + info  
            	page = urllib.urlopen(url)  
            	html = page.read() 
            	dic_json = json.loads(html)  
            	reply_content = dic_json['text']
            	return self.render.reply_text(fromUser,toUser,int(time.time()),reply_content)
            	
            	
                                             
                                             
                                             
                                          
