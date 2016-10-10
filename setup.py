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

user_email = raw_input("Enter Email for App Access: ")
user_phone = raw_input("Enter Phone Number for Phone Updates: ")
newuserKey = "appname"+ ''.join(random.sample((string.ascii_uppercase+string.digits),12)).lower()
target = open("config.json", 'a')

email = '"email":'+'"' +user_email + '",'
key = '"user_key":'+ '"'+newuserKey+'"'
phone = '"phone":'+ '"'+user_phone+'"'

target.write(email)
target.write("\n")
target.write(key)
target.write("\n")
target.write(phone)
target.write("\n")
target.write("}")
target.close()

with open('config.json') as jsonFile:
    data = json.load(jsonFile)
    AK = data["AK"]
    SK = data["SK"]

conn = boto.connect_s3(AK, SK)

bucket = conn.create_bucket(newuserKey)
