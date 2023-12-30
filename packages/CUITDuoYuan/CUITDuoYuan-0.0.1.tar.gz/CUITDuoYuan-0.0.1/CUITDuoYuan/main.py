from question import question


class CUIT:
    all_question = question

    @classmethod
    def get_answer(cls, question):
        ret = []
        for i in cls.all_question:
            if question in i.question_text:
                ret.append(i.answer)

        if len(ret) == 0:
            return '没有题目'
        else:
            return ret
