from django.apps import AppConfig


class ExaminationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'examination'

    verbose_name = '考试相关信息'
