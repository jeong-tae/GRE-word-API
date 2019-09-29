# encoding=utf-8
from quiz_maker import quiz_maker

quiz_maker = quiz_maker("data")

candidates = quiz_maker.create_candid_pool()
for candidate in candidates.items():
	answer, meaning, wrong_answer_list = quiz_maker.make_quiz_meaning(candidate)
	quiz_candid = set(map(lambda x: x[1], wrong_answer_list))
	quiz_candid.add(meaning)

	print(answer)
	print("\n".join(quiz_candid))
	print("ANSWER:", meaning)
	print()
