import boto
import cStringIO
import urllib
from PIL import Image
import boto.s3.connection
from boto.s3.key import Key
import string
import random
import time
from sys import argv
import json
from pprint import pprint
#from obj.json import *##post request test
#url = 'http://myserver/post_service'
#data = dict(name='joe', age='10')

#r = requests.post(url, data=data, allow_redirects=True)
#print r.content
######

#user set up after requirements install
user_email = raw_input("Enter Email for app access: ")
newuserKey = "appname"+ ''.join(random.sample((string.ascii_uppercase+string.digits),12)).lower()
target = open("config.json", 'a') #or json file name

email = '"email":'+'"' +user_email + '",'
key = '"user_key":'+ '"'+newuserKey+'"'

target.write(email)
target.write("\n")
target.write(key)
target.write("\n")
target.write("}")
target.close()

with open('config.json') as jsonFile:
    data = json.load(jsonFile)
    AK = data["AK"]
    SK = data["SK"]
#Now we connect to our s3 bucket and upload from memory
#credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
conn = boto.connect_s3(AK, SK) #json

#Connect to bucket and create key
#using the same key for different images overrites
bucket = conn.create_bucket(newuserKey) #user key
##

