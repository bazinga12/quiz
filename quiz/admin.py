from django.contrib import admin

# Register your models here.

from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
