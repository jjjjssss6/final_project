from django.contrib import admin

# Register your models here.

from .models import StudentExamInfo
from .models import TeacherCorrectionList
from .models import StudentExamFile

admin.site.register(StudentExamInfo)
admin.site.register(TeacherCorrectionList)
admin.site.register(StudentExamFile)