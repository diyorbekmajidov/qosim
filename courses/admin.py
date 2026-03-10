# courses/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Term, Category, Subject, Course, Lesson, Enrollment,
    LessonProgress, Quiz, QuizQuestion, QuizAnswer, Post
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('phone', 'bio', 'avatar')}),
    )


# @admin.register(Term)
# class TermAdmin(admin.ModelAdmin):
#     list_display = ['title', 'order', 'is_active', 'created_at']
#     list_filter = ['is_active', 'created_at']
#     search_fields = ['title', 'description']
#     list_editable = ['order', 'is_active']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'get_courses_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']

    def get_courses_count(self, obj):
        return obj.courses.filter(is_published=True).count()
    get_courses_count.short_description = "Kurslar soni"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['title', 'order', 'duration', 'video_url', 'lecture_file', 'is_free']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'category', 'instructor', 'level', 'order', 'is_published']
    list_filter = ['subject', 'category', 'level', 'is_published']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'order']
    inlines = [LessonInline]
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'subject', 'category', 'description', 'image', 'video_url')
        }),
        ('Kurs parametrlari', {
            'fields': ('instructor', 'duration', 'level', 'price', 'is_free', 'order', 'is_published')
        }),
    )


class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1
    ordering = ['order']


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 2


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'pass_score']
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'quiz', 'order']
    list_filter = ['quiz']
    inlines = [QuizAnswerInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'has_video', 'has_file', 'has_quiz', 'is_free']
    list_filter = ['course', 'is_free']
    search_fields = ['title']
    list_editable = ['order']

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = "Video"

    def has_file(self, obj):
        return bool(obj.lecture_file)
    has_file.boolean = True
    has_file.short_description = "Fayl"

    def has_quiz(self, obj):
        return hasattr(obj, 'quiz')
    has_quiz.boolean = True
    has_quiz.short_description = "Test"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'completed', 'progress']
    list_filter = ['completed', 'enrolled_at']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'quiz_passed', 'completed_at']
    list_filter = ['completed', 'quiz_passed']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}