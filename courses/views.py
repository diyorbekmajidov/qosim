# courses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import Term, Course, Category, Lesson, Post, User
from .serializers import (
    TermSerializer, CourseSerializer, CourseDetailSerializer,
    CategorySerializer, PostSerializer, UserSerializer,
    RegisterSerializer, LoginSerializer
)


# ========================
# TEMPLATE VIEWS (Render)
# ========================

def index(request):
    """Bosh sahifa"""
    courses = Course.objects.filter(is_published=True)[:6]
    posts = Post.objects.filter(is_published=True)[:3]
    context = {
        'courses': courses,
        'posts': posts,
    }
    return render(request, 'index.html', context)


def glossary_page(request):
    """Glossary sahifasi"""
    terms = Term.objects.filter(is_active=True)
    context = {'terms': terms}
    return render(request, 'glossary.html', context)


def courses_page(request):
    """Kurslar sahifasi"""
    courses = Course.objects.filter(is_published=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Search
    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses.html', context)


def course_detail(request, slug):
    """Kurs detallari"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'course_detail.html', context)


def contact_page(request):
    """Aloqa sahifasi"""
    if request.method == 'POST':
        # Contact form logic
        messages.success(request, 'Xabaringiz yuborildi!')
        return redirect('contact')
    return render(request, 'contact.html')


# ========================
# AUTH VIEWS (Template)
# ========================

def login_page(request):
    """Login sahifasi"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Xush kelibsiz!')
            return redirect('index')
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri!')
    
    return render(request, 'login.html')


def register_page(request):
    """Register sahifasi"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password != password2:
            messages.error(request, 'Parollar mos kelmadi!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Bu username band!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Bu email band!')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!')
            return redirect('index')
    
    return render(request, 'register.html')


def logout_view(request):
    """Logout"""
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz!')
    return redirect('index')


@login_required
def profile_page(request):
    """Profil sahifasi"""
    enrollments = request.user.enrollments.all()
    context = {'enrollments': enrollments}
    return render(request, 'profile.html', context)

def handler404(request, exception):
    """404 xato sahifasi"""
    return render(request, '404.html', status=404)

def handler500(request):
    """500 xato sahifasi"""
    return render(request, '500.html', status=500)


# ========================
# REST API VIEWS
# ========================

# User API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    """API Register"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """API Login"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Xush kelibsiz!'
            })
        return Response({
            'error': 'Login yoki parol noto\'g\'ri!'
        }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """API Logout"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Muvaffaqiyatli chiqildi!'})
    except:
        return Response({'error': 'Xatolik'}, status=status.HTTP_400_BAD_REQUEST)


# Glossary API
class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.filter(is_active=True)
    serializer_class = TermSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        terms = self.queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = self.get_serializer(terms, many=True)
        return Response(serializer.data)


# Course API
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_published=True)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# Post API
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = [AllowAny]