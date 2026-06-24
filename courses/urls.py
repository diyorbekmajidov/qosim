# courses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'terms', views.TermViewSet, basename='term')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # ========================
    # TEMPLATE URLS
    # ========================
    path('', views.index, name='index'),
    path('glossary/', views.glossary_page, name='glossary'),

    # Fanlar
    path('subjects/', views.subjects_page, name='subjects'),
    path('subject/<slug:slug>/', views.subject_detail, name='subject_detail'),

    # Kurslar
    path('courses/', views.courses_page, name='courses'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),

    # Darslar
    path('lesson/<int:pk>/', views.lesson_view, name='lesson'),
    path('lesson/<int:pk>/complete/', views.mark_lesson_complete, name='lesson_complete'),
    path('lesson/<int:pk>/quiz/', views.quiz_submit, name='quiz_submit'),

    path('contact/', views.contact_page, name='contact'),

    # Auth URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),

    # ========================
    # NEW SECTIONS
    # ========================
    path('games/', views.games_page, name='games'),
    path('about/', views.about_page, name='about'),
    path('assignments/', views.assignments_page, name='assignments'),
    path('assignment/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('references/', views.references_page, name='references'),
    path('final-tests/', views.final_test_list, name='final_test_list'),
    path('final-test/<int:pk>/', views.final_test_detail, name='final_test_detail'),

    # ========================
    # API URLS
    # ========================
    path('api/', include(router.urls)),
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
]