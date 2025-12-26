# courses/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# ========================
# USER MODEL
# ========================
class User(AbstractUser):
    """Custom User Model"""
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
    
    def __str__(self):
        return self.username


# ========================
# GLOSSARY MODEL
# ========================
class Term(models.Model):
    """Lug'at atamasi - CKEditor bilan"""
    title = models.CharField(max_length=200, verbose_name="Atama")
    description = RichTextField(verbose_name="Ta'rif", config_name='default')  # CKEditor
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Atama"
        verbose_name_plural = "Atamalar"
    
    def __str__(self):
        return self.title


# ========================
# COURSE MODELS
# ========================
class Category(models.Model):
    """Kurs kategoriyalari"""
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icon class")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Kurslar"""
    title = models.CharField(max_length=200, verbose_name="Kurs nomi")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    description = RichTextField(verbose_name="Tavsif", config_name='default')
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')
    duration = models.CharField(max_length=50, verbose_name="Davomiyligi")
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Murakkab'),
    ], default='beginner')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False, verbose_name="Bepul")
    is_published = models.BooleanField(default=False, verbose_name="Nashr qilingan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
    
    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Darslar"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200, verbose_name="Dars nomi")
    content = RichTextField(verbose_name="Dars matni", config_name='default')
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
    order = models.IntegerField(default=0)
    duration = models.CharField(max_length=20, blank=True)
    is_free = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    """Kursga yozilganlar"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0, verbose_name="Foiz")
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name = "Yozilgan"
        verbose_name_plural = "Yozilganlar"
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


# ========================
# BLOG/NEWS MODEL
# ========================
class Post(models.Model):
    """Maqolalar/Yangiliklar"""
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True)
    content = RichTextField(verbose_name="Matn", config_name='default')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
    
    def __str__(self):
        return self.title