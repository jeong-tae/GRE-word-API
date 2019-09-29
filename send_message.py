import os
from slacker import Slacker

token = os.environ["SLACK_BOT_TOKEN"]
slack = Slacker(token)

moreInfo = ['person', 'person1', 'person2']
message = [
	{
		"title": "Lunch time has been decided",
		"text": "You will also be joining",
		"actions": [
			{
				"name": "buttonName",
				"text": "More Info",
				"type": "button",
				"value": moreInfo
			}
		]
	}
]

message = [
	{
        "title": "Book flight",
	    "text": "<@W1A2BC3DD> approved your travel request. Book any airline you like by continuing below.",
		"fallback": "Book your flights at https://flights.example.com/book/r123456",
		"actions": [
		    {
			    "type": "button",
			    "text": "Book flights",
		        "url": "https://flights.example.com/book/r123456",
                "style": "primary"
			},
            {
                "type": "button",
                "text": "Cancel trabel request",
                "url": "https://requests.example.com/cancel/r123456",
                "style": "danger"
            }
		]
	}
]

slack.chat.post_message("#general", 'URL Test :bug:', attachments=message)
