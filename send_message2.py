from flask import Flask, request, make_response, Response
import os
import slack

client = slack.WebClient(token = os.environ["SLACK_BOT_TOKEN"])
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_BOT_TOKEN"]
app = Flask(__name__)

def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)


@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    verify_slack_token(form_json["token"])

    menu_options = {
        "options": [
            {
                "text": "Chess",
                "value": "chess"
            },
            {
                "text": "Global Thermonuclear War",
                "value": "war"
            }
        ]
    }
    return Response(json.dumps(menu_options), mimetype='application/json')

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "war":
        message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
    else:
        message_text = ":horse:"

    response = client.postMessage(
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text=message_text,
      attachments=[]
    )

    return make_response("", 200)

message_attachments = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "game",
                "text": "War game",
                "type": "button",
                #"data_source": "external"
                "value": "war"
            },
            {
                "name": "game",
                "text": "Chess",
                "type": "buttone",
                "value": "chess"
            }
        ]
    }
]

client.chat_postMessage(
    channel="#general",
    text="GRE test",
    attachments=message_attachments
)

if __name__ == "__main__":
    app.run()
