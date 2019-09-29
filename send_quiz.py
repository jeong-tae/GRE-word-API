import os
from slacker import Slacker
from GRE_quiz.quiz_maker import quiz_maker
import sys
import time

token = os.environ["SLACK_BOT_TOKEN"]
slack = Slacker(token)
quiz_maker = quiz_maker("GRE_quiz/data")
moreInfo = ['person', 'person1', 'person2']
candidates = quiz_maker.create_candid_pool()
question_type = sys.argv[1]

def make_action_form(target, candid, text_type):
    msg_qa = ("Correct!", "#339CFF") if candid[0] == target[0] else ("Wrong!", "#FF4B33")
    if text_type == "word": 
        candid_text = candid[0]
    elif text_type == "meaning": 
        candid_text = candid[1]
    else: 
        return
    msg_cand_mean = {
            "name": text_type,
            "type": "button",
            "text": candid_text,
            "style": "primary",
            "value": candid_text,
            "confirm": {
                "title": msg_qa[0],
                "color": msg_qa[1], 
                "text": "    ".join(candid_info),
                }
            }
    return msg_cand_mean

for candidate in candidates.items():
    target_word, meaning, wrong_answer_list = quiz_maker.make_quiz_meaning(candidate)
    target_info = [target_word, meaning]
    quiz_candids = set(map(lambda x: (x[0],x[1]), wrong_answer_list))
    quiz_candids.add((target_word,meaning))
    print(quiz_candids)
    message = dict()
    if question_type == "word":
        message["title"] = meaning
    elif question_type == "meaning":
        message["title"] = target_word
    message["actions"] = []
    for q_candid_w, q_candid_m in quiz_candids:
        candid_info = [q_candid_w, q_candid_m]
        msg_cand_mean = make_action_form(target_info, candid_info, text_type=question_type)
        message["actions"].append(msg_cand_mean)
    clock = time.localtime(time.time())
    current_time = "%s-%s-%s-%s:%s" % (clock.tm_year,clock.tm_mon,clock.tm_mday,clock.tm_hour,clock.tm_min)
    slack.chat.post_message("#education-study", '[%s] GRE Daily Quiz - %s' % (current_time, question_type.upper()), attachments=[message])
    break
