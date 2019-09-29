import os
import slack

from send_quiz import make_message
quiz_type = ['word', 'meaning', 'cloze', 'synonyms']

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

    text = data.get('text', '').lower()
    channel_id = data['channel']

    if text in quiz_type:

        attachments = make_message(text)
        #user = data['user']

        for attachment in attachments:
            web_client.chat_postMessage(
                channel=channel_id,
                text = "GRE Quiz - %s"%text.upper(),
                attachments=attachments[0],
                #thread_ts=thread_ts
            )
    else:
        web_client.chat_postMessage(
            channel=channel_id,
            #text = "Invalid text, can't recognize command: %s\n Type command in [%s]" % (text, ', '.join(quiz_type))
            text = "asdfasdf??",
            attachments=[]
        )


if __name__ == "__main__":
    slack_token = os.environ["SLACK_API_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
