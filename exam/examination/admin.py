from django.contrib import admin

# Register your models here.

from .models import Examination
from .models import ExamPaper
from .models import Question
from .models import PaperIncludingQuestions
from .models import TestSet


admin.site.register(Examination)
admin.site.register(ExamPaper)
admin.site.register(Question)
admin.site.register(PaperIncludingQuestions)
admin.site.register(TestSet)


