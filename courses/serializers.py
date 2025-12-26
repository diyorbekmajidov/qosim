# courses/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Term, Course, Category, Lesson, Enrollment, Post

User = get_user_model()

# ========================
# USER SERIALIZERS
# ========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'bio', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, 
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 
                  'first_name', 'last_name', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi!"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# ========================
# GLOSSARY SERIALIZERS
# ========================
class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['id', 'title', 'description', 'created_at', 'order', 'is_active']


# ========================
# COURSE SERIALIZERS
# ========================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'duration', 'is_free']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'category', 'description', 'image',
                  'instructor', 'duration', 'level', 'price', 'is_free', 
                  'lessons_count', 'created_at']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'category', 'description', 'image',
                  'instructor', 'duration', 'level', 'price', 'is_free', 
                  'lessons', 'created_at']


# ========================
# POST SERIALIZERS
# ========================
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'image', 
                  'is_published', 'created_at']