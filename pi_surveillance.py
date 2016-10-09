from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import urllib
import urllib2
import cStringIO
import boto
from PIL import Image
from pytz import timezone
from twilio.rest import TwilioRestClient
import pyimgur

twC = TwilioRestClient("AC80efee41b1fa30335d88ff84ea94df0f","62759ad9bb64eb76d2716f420e532df8")
imgC = "f4c8af478ac86b8"
imG = pyimgur.Imgur(imgC)

with open('conf.json') as jsonFile:
    data = json.load(jsonFile)
    email = data["email"]
    userKey = data["user_key"]
    AK = data["AK"]
    SK = data["SK"]
    phone = data["phone"]
 
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())
 
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))


camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
 
print "[INFO] warming up..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now(timezone('US/Mountain'))
motionCounter = 0

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = f.array
	timestamp = datetime.datetime.now(timezone('US/Mountain'))
	text = "Unoccupied"
 
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	if avg is None:
		print "[INFO] starting background model..."
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue
 
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	for c in cnts:
		if cv2.contourArea(c) < conf["min_area"]:
			continue
 
		(x, y, w, h) = cv2.boundingRect(c)
		text = "Occupied"
 
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	if text == "Occupied":
		if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			motionCounter += 1
 
			if motionCounter >= conf["min_motion_frames"]:
				
				t = TempImage(basePath="/tmp/")
				timestampd = datetime.datetime.now(timezone('US/Mountain'))
				date = timestampd.strftime("%A %d %B %Y %I:%M:%S%p")
				cv2.imwrite(t.path, frame)
				# upload the image to S3 and cleanup the tempory image
				print "[UPLOAD] {}".format(ts)
				url = t.path
				uploaded_image = imG.upload_image(url, title=date)
				#twilio message
				print conf["min_sms_seconds"]
				twC.messages.create(from_="(720) 903-4624", to=phone,body="Recent Activity Alert at Galvanize. Check App for More Details.",media_url=uploaded_image.link)
				print url
				fp = urllib.urlopen(url)
				img = cStringIO.StringIO(fp.read())
				im = Image.open(img)
				im2 = im.resize((500, 500), Image.NEAREST)
				out_im2 = cStringIO.StringIO()
				im2.save(out_im2, 'PNG')
				conn = boto.connect_s3(AK, SK)
				b = conn.get_bucket(userKey)
 				b.set_acl('public-read-write')
				print date
				k = b.new_key(date)
				k.set_contents_from_string(out_im2.getvalue())
				t.cleanup()
 
				lastUploaded = timestamp
				motionCounter = 0
 
	else:
		motionCounter = 0

	if conf["show_video"]:
		cv2.imshow("Security Feed", frame)
		key = cv2.waitKey(1) & 0xFF
 
		if key == ord("q"):
			break
 
	rawCapture.truncate(0)
