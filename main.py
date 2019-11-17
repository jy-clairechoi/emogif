from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
import random

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # yay i did work too
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    print(body)

    pre_json = {
		"documents": [
			{
            	"language": "en",
            	"id": "1",
            	"text": body
        	}
        ]
    }

    url = "https://texttwilioapp.cognitiveservices.azure.com/text/analytics/v2.1/sentiment"

    payload = json.dumps(pre_json)
    headers = {
    'Ocp-Apim-Subscription-Key': "ed8df32a3e4346edb932b5cf40973888",
    'Content-Type': "application/json",
    'Accept': "application/json",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "d6e09457-12e9-4186-9901-825344d5b213,97dc2ad9-d3e9-4048-a8ce-e76c09cb41eb",
    'Host': "texttwilioapp.cognitiveservices.azure.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "185",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    response_obj = response.json()
    score = response_obj["documents"][0]["score"]
    
    emotion = None
    
    if score>0.80:
    	emotion = 'Excited'
    elif score> 0.60:
    	emotion = 'Happy'
    elif score>0.40:
    	emotion = 'Content'
    elif score>0.20:
    	emotion ='Sad'
    else:
    	emotion = 'Depressed'

    url = "http://api.giphy.com/v1/gifs/search"
    querystring = {"api_key":"0HR7762cOExxa7GWZ8aIQlKevuHkLmz0","q":emotion, "limit": "20"}
    headers = {
		'User-Agent': "PostmanRuntime/7.19.0",
		'Accept': "*/*",
	    'Cache-Control': "no-cache",
	    'Postman-Token': "8dba5749-8eb5-424e-a026-6fa97f2cc4e0,fca7f2ee-9628-48e3-af5e-649ebf75d912",
	    'Host': "api.giphy.com",
	    'Accept-Encoding': "gzip, deflate",
	    'Connection': "keep-alive",
	    'cache-control': "no-cache"
    }
    response_gif = requests.request("GET", url, headers=headers, params=querystring)
    response_obj_gif = response_gif.json()
    num = random.randint(0, 19)
    url = response_obj_gif["data"][num]["url"]
    


    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message(url)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)