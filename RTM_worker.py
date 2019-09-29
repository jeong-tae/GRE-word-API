import os
import slack

from send_quiz import make_message
quiz_types = ['cloze', 'synonyms', 'meaning', 'word']

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

    user_message = data.get('text', '').lower()

    if "user" in data:
        print("Got message: %s"%user_message)
    else:
        return

    if user_message in quiz_types:
        channel_id = data['channel']
        attachments = make_message(user_message)

        web_client.chat_postMessage(
            channel=channel_id,
            text = "GRE Quiz - %s"%user_message,
            attachments=attachments,
        )
    #print("User: %s"%data['user'])

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
