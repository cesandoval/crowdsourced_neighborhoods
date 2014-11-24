import json 
import requests
import time
import requests
import threading


## You need to change this to your own info
Client_ID = '9056a11deaef47a59abc8647208b58d7'
Redirect_URI = 'http://www.nytimes.com'
code='0340b48b153c4a4b99fe0f8b328a717a'
access_token = '23252351.9056a11.93d34bc129f443cba0adef6de1532f8f'


def getfeed():
	threading.Timer(120.0, getfeed).start()

	t = time.strftime("%Y%m%d%H%M")
	# print t
	with open('ID') as f:
	    ID = f.read().splitlines()
	data = [None]*len(ID)
	counter = 0
	for item in ID[0:15]:
		url = 'https://api.instagram.com/v1/locations/'+str(item)+'/media/recent?access_token='+access_token
		# print url
		r = requests.get(str(url))
		data[counter] = r.json()

		counter += 1
	with open('instagram/feed'+t+'.json','a') as f: 
	 	json.dump(data, f)
try: getfeed()
except: pass

# t = threading.Timer(60.0, getfeed)
# t.start()
