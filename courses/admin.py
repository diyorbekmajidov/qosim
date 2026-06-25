from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Term, AboutPage, Category, Subject, Course, Lesson, Enrollment,
    LessonProgress, Quiz, QuizQuestion, QuizAnswer, Post,
    PracticalAssignment, AssignmentSubmission, Reference,
    FinalTest, FinalTestQuestion, FinalTestAnswer, FinalTestResult
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('phone', 'bio', 'avatar')}),
    )


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('full_name', 'position', 'bio_short', 'photo')
        }),
        ('Statistika', {
            'fields': ('experience_years', 'students_count', 'publications_count', 'courses_count')
        }),
        ('Biografiya', {
            'fields': ('education_text', 'career_text', 'science_text', 'online_text'),
            'classes': ('collapse',),
        }),
        ('Ko\'nikmalar', {
            'fields': (
                'skill1_name', 'skill1_percent',
                'skill2_name', 'skill2_percent',
                'skill3_name', 'skill3_percent',
                'skill4_name', 'skill4_percent',
            ),
            'classes': ('collapse',),
        }),
        ('Bog\'lanish', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Tadqiqot yo\'nalishlari', {
            'fields': ('research_topics',)
        }),
    )

    def has_add_permission(self, request):
        # Faqat bitta yozuv bo'lishi uchun — allaqachon bor bo'lsa qo'shishga ruxsat yo'q
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

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


class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission
    extra = 0
    readonly_fields = ['user', 'submission_file', 'comment', 'submitted_at']
    fields = ['user', 'submission_file', 'status', 'score', 'feedback', 'submitted_at']


@admin.register(PracticalAssignment)
class PracticalAssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'max_score', 'deadline_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    inlines = [AssignmentSubmissionInline]
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('lesson', 'title', 'description', 'task_file', 'canva_url')
        }),
        ('Parametrlar', {
            'fields': ('max_score', 'deadline_days', 'is_active')
        }),
    )


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignment', 'status', 'score', 'submitted_at', 'download_file']
    list_filter = ['status', 'submitted_at']
    search_fields = ['user__username', 'assignment__title']
    list_editable = ['status', 'score']
    readonly_fields = ['user', 'assignment', 'submission_file', 'comment', 'submitted_at', 'download_link']
    fieldsets = (
        ('Yuborilgan ish', {
            'fields': ('user', 'assignment', 'submission_file', 'download_link', 'comment', 'submitted_at')
        }),
        ('Baholash', {
            'fields': ('status', 'score', 'feedback')
        }),
    )

    def download_file(self, obj):
        from django.utils.html import format_html
        if obj.submission_file:
            return format_html(
                '<a href="{}" download style="background:#0d6efd;color:white;padding:4px 10px;border-radius:4px;text-decoration:none;font-size:12px;">⬇ Yuklab olish</a>',
                obj.submission_file.url
            )
        return '—'
    download_file.short_description = 'Fayl'
    download_file.allow_tags = True

    def download_link(self, obj):
        from django.utils.html import format_html
        if obj.submission_file:
            return format_html(
                '<a href="{}" download class="button">⬇ Faylni yuklab olish</a>',
                obj.submission_file.url
            )
        return 'Fayl yuklanmagan'
    download_link.short_description = 'Faylni yuklab olish'


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'year', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'authors']
    list_editable = ['order', 'is_active', 'category']


# ========================
# FINAL TEST ADMIN
# ========================
class FinalTestAnswerInline(admin.TabularInline):
    model = FinalTestAnswer
    extra = 3
    fields = ['text', 'is_correct']


class FinalTestQuestionInline(admin.StackedInline):
    model = FinalTestQuestion
    extra = 1
    ordering = ['order']
    show_change_link = True


@admin.register(FinalTest)
class FinalTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'pass_score', 'get_questions_count', 'is_active', 'order', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    inlines = [FinalTestQuestionInline]
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'description', 'pass_score', 'order', 'is_active')
        }),
    )

    def get_questions_count(self, obj):
        return obj.questions.count()
    get_questions_count.short_description = "Savollar soni"


@admin.register(FinalTestQuestion)
class FinalTestQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'test', 'order']
    list_filter = ['test']
    search_fields = ['question']
    inlines = [FinalTestAnswerInline]
    ordering = ['test', 'order']


@admin.register(FinalTestResult)
class FinalTestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'correct', 'total', 'passed', 'completed_at']
    list_filter = ['passed', 'test', 'completed_at']
    search_fields = ['user__username', 'test__title']
    readonly_fields = ['user', 'test', 'score', 'correct', 'total', 'passed', 'completed_at']