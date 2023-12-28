import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.0

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from phpthon import *
elif version_info[0] == 3: # Python 3.x
    from phpthon.phpthon import *



import urllib.request
import mimetypes
import ssl
import os
try:
    import requests
except ImportError:
    try:
        os.system("pip install requests")
    except:
        try:
            os.system("pip3 install requests")
        except:
            try:
                os.system("python3 -m pip install requests")
            except:
                os.system("python -m pip install requests")
    import requests
import json
import re
from random import randint
from subprocess import check_output as chk

def detect_file_format(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64)"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content_type = response.headers.get('Content-Type')
    file_extension = mimetypes.guess_extension(content_type)

    if file_extension:
        return file_extension.lstrip('.')
    else:
        return None

def file_get_contents(name):
    if name.startswith("http://") or name.startswith("https://"):
        return requests.get(name).text
    else:
        file=open(name,"r")
        contents=file.read()
        file.close()
        return contents

def file_put_contents(name,contents):
    file=open(name,"w")
    file.write(contents)
    file.close()
    return True

def filesize(file):
    # get file size in python

    file_name = file

    file_stats = os.stat(file_name)
    return file_stats.st_size

def file_link_size(link):
    ssl._create_default_https_context = ssl._create_unverified_context
    site = urllib.request.urlopen(link)
    meta = site.info()
    file_size = int(site.getheader('Content-Length'))
    return file_size

def json_encode(js):
    try:
        return json.dumps(js)
    except:
        raise("Failed To Encode json!")

def json_decode(js):
    try:
        return json.loads(js)
    except:
        raise("Failed To Decode json!")

def rand(start,end):
    return str(randint(int(start),int(end)))

def preg_match(match,string):
    return re.search(match,string)

def explode(sett,string):
    return string.split(sett)

def isset(inputstr):
    if inputstr == "":
        return False
    else:
        return True
def substr(text,num):
    return text[int(num):]

def strpos(string,find):
    return find in string

def shell_exec(cmd):
    try:
        return chk(cmd,shell=True).decode()
    except Exception as er:
        return str(er)
    
