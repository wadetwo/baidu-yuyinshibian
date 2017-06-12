#!/user/bin/env python
# -*- coding: utf-8 -*-
#from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave
import time
import urllib,urllib2,pycurl
import base64
import json
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = "yuyin.wav"
duihua = '1'

def gethtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def get_token():
	apiKey = "Ll0c53MSac6GBOtpg22ZSGAU"
	secretKey = "44c8af396038a24e34936227d4a19dc2"
	auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
	res = urllib.urlopen(auth_url)
	json_data = res.read()
	return json.loads(json_data)["access_token"]

def dump_res(buf):
	global duihua
	print "string type"
	print (buf)
	a=eval(buf)
	print type(a)
	if a['err_msg']=='success':
		duihua = a['result'][0]
		print duihua

def use_cloud(token):
	fp = wave.open(filename, 'rb')
	nf = fp.getnframes()
	f_len = nf * 2
	audio_data = fp.readframes(nf)
	cuid = "9724741"
	srv_url = 'http://vop.baidu.com/server_api?'+'cuid='+cuid+'&token='+token
	http_header = [
		'Content-Type: audio/pcm; rate=8000',
		'Content-Length: %d' % f_len
	]
	c = pycurl.Curl()
	c.setopt(pycurl.URL, str(srv_url))
	c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
	c.setopt(c.POST, 1)
	c.setopt(c.CONNECTTIMEOUT, 30)
	c.setopt(c.TIMEOUT, 30)
	c.setopt(c.WRITEFUNCTION, dump_res)
	c.setopt(c.POSTFIELDS, audio_data)
	c.setopt(c.POSTFIELDSIZE, f_len)
	c.perform()
def save_wave_file(filename, data):
	wf = wave.open(filename,'wb')
	wf.setnchannels(1)
	wf.setsampwidth(2)
	wf.setframerate(SAMPLING_PATE)
	wf.writeframes("".join(data))
	wf.close()

token = get_token()
key = '7b64483719454a93a7ac2a61343d1d69'
api = 'http://www.tuling123.com/openapi/api?key='+key+'&info='

while True:
	os.system('arecord -D "plughw:1,0" -f S16_LE -d 5 -r 8000 /home/pi/Documents/python/baidu-yuyinshibian/yuyin.wav')
	use_cloud(token)
	print duihua
	info = duihua
	request = api+info
	response = gethtml(request)
	dic_json = json.loads(response)
	a = dic_json['text']
	print type(a)
	unicodestring = a
	uf8string = unicodestring.encode("utf-8")
	print type(uf8string)
	print str(a)
	url = "http://tsn.baidu.com/text2audio?tex="+dic_json['text']+"&lan=zh&per=0&pit=8&spd=7&vol=8&cuid=9724741&ctp=1&tok="+token
	os.system('mpg123 "%s"'%(url))	 
