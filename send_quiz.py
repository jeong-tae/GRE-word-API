import os
from slacker import Slacker
from GRE_quiz.quiz_maker import quiz_maker
import sys
import time

token = os.environ["SLACK_BOT_TOKEN"]
slack = Slacker(token)
quiz_maker = quiz_maker("GRE_quiz/data")
question_type = sys.argv[1]
quiz_maker.update_question_type(question_type)

def make_title_text(target, q_type, question=None):
    if q_type is "word":
        return target[0]
    elif q_type is "meaning":
        return target[1]
    elif q_type in ["cloze", "synonyms"]:
        return question 

def make_action_form(target, candid, q_type):
    if q_type == "meaning": 
        idx = 1
    else:
        idx = 0
    msg_qa = ("Correct!", "#339CFF") if candid[idx] == target[idx] else ("Wrong!", "#FF4B33")
    msg_cand_mean = {
            "name": q_type,
            "type": "button",
            "text": candid[idx],
            "style": "primary",
            "value": candid[idx],
            "confirm": {
                "title": msg_qa[idx],
                "color": msg_qa[idx], 
                "text": "    ".join(candid_info),
                }
            }
    return msg_cand_mean

if question_type in ["word", "meaning"]:
    make_quiz_ft = quiz_maker.make_quiz_meaning
elif question_type == "cloze":
    make_quiz_ft = quiz_maker.make_quiz_cloze
elif question_type == "synonyms":
    make_quiz_ft = quiz_maker.make_quiz_synonyms
else:
    raise(ValueError, "Type the question type: word, meaning, cloze, synonyms")

candidates = quiz_maker.create_candid_pool()

for candidate in candidates.items():
    message = dict()
    target_info, wrong_answer_list, question = make_quiz_ft(candidate)
    quiz_candids = set(map(lambda x: (x[0],x[1]), wrong_answer_list))
    quiz_candids.add(target_info)
    message["title"] = make_title_text(target_info, question_type, question=question)
    message["actions"] = []
    for candid_info in quiz_candids:
        msg_cand_mean = make_action_form(target_info, candid_info, question_type)
        message["actions"].append(msg_cand_mean)
    clock = time.localtime(time.time())
    current_time = "%s-%s-%s-%s:%s" % (clock.tm_year,clock.tm_mon,clock.tm_mday,clock.tm_hour,clock.tm_min)
    slack.chat.post_message("#daily_quiz", '[%s] GRE Daily Quiz - %s' % (current_time, question_type.upper()), attachments=[message])
    break
