from datetime import date, datetime
import json
from examination.models import PaperIncludingQuestions

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def GetPaperQuesById(id):
    try:
        paper_ques_detail = PaperIncludingQuestions.objects.filter(id=id).values()[0]
        return paper_ques_detail
    except Exception:
        return '获取试卷题目信息失败'
