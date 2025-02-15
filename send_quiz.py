import os
from slacker import Slacker
from quiz_maker import quiz_maker
import sys
import time

token = os.environ["SLACK_API_TOKEN"]
slack = Slacker(token)

class quiz_sender(object):
    def __init__(self, data_dir):
        self.quiz_maker = quiz_maker(data_dir)

    def make_title_text(self, target, q_type, question=None):
        if q_type == "word":
            return target[1]
        elif q_type == "meaning":
            return target[0]
        elif q_type in ["cloze", "synonyms"]:
            return question 

    def make_action_form(self, target, candid, q_type):
        if q_type == "meaning": 
            idx = 1
        else:
            idx = 0
        msg_qa = "Your are good! Correct! =)" if candid[idx] == target[idx] else "Try again..."
        msg_cand_mean = {
                "name": q_type,
                "type": "button",
                "text": candid[idx],
                "style": "default",
                "value": candid[idx],
                "confirm": {
                    "title": msg_qa,
                    "text": "    ".join(candid),
                    "dismisss_text": "Skip"
                    }
                }
        return msg_cand_mean

    def make_message(self,question_type):
        self.quiz_maker.update_question_type(question_type)
        if question_type in ["word", "meaning"]:
            make_quiz_ft = self.quiz_maker.make_quiz_meaning
        elif question_type == "cloze":
            make_quiz_ft = self.quiz_maker.make_quiz_cloze
        elif question_type == "synonyms":
            make_quiz_ft = self.quiz_maker.make_quiz_synonyms
        elif question_type == "study":
            message = dict()
            target_word, meaning, similar_words = self.quiz_maker.make_study_synonyms()
            tmp = list(map(lambda x: "%s: %s" % (x[0][0], "; ".join(map(lambda y: y[1], x))), similar_words))
            message["title"] = "%s: %s\n\n %s" % (target_word, meaning, "\n\n".join(tmp))
            return [message]
        else:
            raise(ValueError, "Type the question type: word, meaning, cloze, synonyms, priority, study")

        candidates = self.quiz_maker.create_candid_pool()
        message_list = []

        for candidate in candidates.items():
            message = dict()
            target_info, wrong_answer_list, question = make_quiz_ft(candidate)
            quiz_candids = set(map(lambda x: (x[0],x[1]), wrong_answer_list))
            quiz_candids.add(target_info)
            message["title"] = "*%s*" % self.make_title_text(target_info, question_type, question=question)
            message["actions"] = []
            for candid_info in quiz_candids:
                msg_cand_mean = self.make_action_form(target_info, candid_info, question_type)
                message["actions"].append(msg_cand_mean)
            message_list.append(message)
        return message_list

if __name__=="__main__":
    question_type = sys.argv[1].lower()
    if question_type == "priority":
        qm = quiz_sender("./data/priority") 
        messages = qm.make_message("meaning")
        slack.chat.post_message("#daily_quiz", 'GRE Daily Quiz - %s' % (question_type.upper()), attachments=messages)
        messages = qm.make_message("word")
        slack.chat.post_message("#daily_quiz", 'GRE Daily Quiz - %s' % (question_type.upper()), attachments=messages)
    else:
        qm = quiz_sender("./data/day*") 
        messages = qm.make_message(question_type)
        slack.chat.post_message("#daily_quiz", 'GRE Daily Quiz - %s' % (question_type.upper()), attachments=messages)
    
