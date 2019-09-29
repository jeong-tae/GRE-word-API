


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
    msg_qa = ("Correct!", "#339CFF") if candid[idx] == target[idx] else ("Wrong!", "#FF4B33")
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
