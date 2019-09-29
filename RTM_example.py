import os
import slack

@slack.RTMClient.run_on(event='member_joined_channel')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    channel_id = data['channel']
    user = data['user']

    if 'general' in channel_id:
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!, To start test, please DM 'test' \With any bot problem, contact <@jtlee> or <@eunbyul Kim>",
        )

@slack.RTMClient.run_on(event='message')
def word_test(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']

    text = data.get('text', '')

    '''
    message_attachments = [
        {
            "text": "Choose a game to play",
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "Chess",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "game",
                    "text": "Falken's Maze",
                    "type": "button",
                    "value": "maze"
                },
                {
                    "name": "game",
                    "text": "Thermonuclear War",
                    "style": "danger",
                    "type": "button",
                    "value": "war",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Wouldn't you prefer a good game of chess?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }
            ]
        }
    ]
	'''
    message_attachments = [	
        {
            "text": "Choose a game to play",
            "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "callback_id": "game_selection",
            "actions": [
                {
                    "name": "games_list",
                    "text": "Pick a game...",
                    "type": "select",
                    "options": [
                        {
                            "text": "Chess",
                            "value": "chess"
                        },
                        {
                            "text": "Bridge",
                            "value": "bridge"
                        },
                        {
                            "text": "Checkers",
                            "value": "checkers"
                        },
                        {
                            "text": "Poker",
                            "value": "poker"
                        },
                        {
                            "text": "Falken's Maze",
                            "value": "maze"
                        },
                        {
                            "text": "Global Thermonuclear War",
                            "value": "war"
                        }
                    ]

                }
            ],
            "original_message": {
                "text": "Simple test",
                "attachments": [
                    {
                        "callback_id": "game_selection",
                        "color": "3AA3E3",
                        "actions": [
                            {
                                "id": "1",
                                "name": "games_list",
                                "text": "GAME!!",
                                "data_source": "options"
                            }
                        ]
                    }
                ]
            }
        }
	]

    if 'word' in text.lower() or 'test' in text.lower():
        channel_id = data['channel']
        #thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text = "Do you wannt play?",
            attachments=message_attachments,
            #thread_ts=thread_ts
        )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
