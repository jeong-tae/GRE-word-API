import os
from slacker import Slacker
from GRE_quiz.quiz_maker import quiz_maker
import sys
import time

token = os.environ["SLACK_API_TOKEN"]
slack = Slacker(token)
quiz_maker = quiz_maker("GRE_quiz/data")

def make_title_text(target, q_type, question=None):
    if q_type == "word":
        return target[1]
    elif q_type == "meaning":
        return target[0]
    elif q_type in ["cloze", "synonyms"]:
        return question 

def make_action_form(target, candid, q_type):
    if q_type == "meaning": 
        idx = 1
    else:
        idx = 0
    msg_qa = ("Your are good! Correct! =)", "#339CFF") if candid[idx] == target[idx] else ("Try again...", "#FF4B33")
    msg_cand_mean = {
            "name": q_type,
            "type": "button",
            "text": candid[idx],
            "style": "default",
            "value": candid[idx],
            "confirm": {
                "title": msg_qa[0],
                "color": msg_qa[1], 
                "text": "    ".join(candid),
                "dismisss_text": "Skip"
                }
            }
    return msg_cand_mean

def make_message(question_type):
    quiz_maker.update_question_type(question_type)


    if question_type in ["word", "meaning"]:
        make_quiz_ft = quiz_maker.make_quiz_meaning
    elif question_type == "cloze":
        make_quiz_ft = quiz_maker.make_quiz_cloze
    elif question_type == "synonyms":
        make_quiz_ft = quiz_maker.make_quiz_synonyms
    else:
        raise(ValueError, "Type the question type: word, meaning, cloze, synonyms")

    candidates = quiz_maker.create_candid_pool()
    message_list = []

    for candidate in candidates.items():
        message = dict()
        target_info, wrong_answer_list, question = make_quiz_ft(candidate)
        quiz_candids = set(map(lambda x: (x[0],x[1]), wrong_answer_list))
        quiz_candids.add(target_info)
        message["title"] = "*%s*" % make_title_text(target_info, question_type, question=question)
        message["actions"] = []
        for candid_info in quiz_candids:
            msg_cand_mean = make_action_form(target_info, candid_info, question_type)
            message["actions"].append(msg_cand_mean)
        message_list.append(message)
    return message_list

if __name__=="__main__":
    question_type = sys.argv[1].lower()
    messages = make_message(question_type)
    slack.chat.post_message("#daily_quiz", 'GRE Daily Quiz - %s' % (question_type.upper()), attachments=messages)
