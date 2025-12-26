# courses/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'terms', views.TermViewSet, basename='term')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    # ========================
    # TEMPLATE URLS
    # ========================
    path('', views.index, name='index'),
    path('glossary/', views.glossary_page, name='glossary'),
    path('courses/', views.courses_page, name='courses'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('contact/', views.contact_page, name='contact'),
    
    # Auth URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    
    # ========================
    # API URLS
    # ========================
    path('api/', include(router.urls)),
    path('api/auth/register/', views.api_register, name='api_register'),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
]