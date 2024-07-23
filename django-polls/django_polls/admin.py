from django.contrib import admin
from .models import Choice, Question


# class ChoiceInline(adminxxx.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Name", {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


#adminxxx.site.register(Question, QuestionAdmin)
#adminxxx.site.register(Choice)
admin.site.register(Question, QuestionAdmin)