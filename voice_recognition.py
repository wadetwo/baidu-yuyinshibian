#!/user/bin/env python
# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
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
sys.setdefaultcoding("utf-8")

save_count = 0
save_buffer = []
t = 0
sum = 0
time_flag = 0
flag_num = 0
filename = "2.wav"
duihua = '1'

def gethtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def get_token():
	apiKey = "Ll0c53MSac6GBOtpg22ZSGAU"
	secretKey = "44c8af396038a24e34936227d4a19dc2"
	auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;
	res = urllib.urlopen(auth_url)
	json_data = res.read()
	return json.loads(json_data)["acces_token"]
ll
