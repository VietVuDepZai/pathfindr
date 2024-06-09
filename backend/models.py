from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils import timezone

class THCS(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images", default="/images/placeholder.png")
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(self.headline)
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)

class Studenddt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    hoten = models.CharField(max_length=2000, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    mobile = models.CharField(max_length=20, default=None, null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    khoihoc = models.CharField(max_length=200, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    @property
    def get_name(self):
        return str(self.hoten)

    def __str__(self):
        return str(self.hoten)

class PostComment(models.Model):
    author = models.ForeignKey(Studenddt, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
class DienDan(models.Model):
    author = models.ForeignKey(Studenddt, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.author.school
class Result(models.Model):
    tester = models.ForeignKey(Studenddt,on_delete=models.CASCADE, default=None,null=True, blank=True)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    khoihoc=models.CharField(max_length=1900, null=True, blank=True)
class DienDanComment(models.Model):
    author = models.ForeignKey(Studenddt, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(DienDan, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
class XetDiemChuyen(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    mobile = models.CharField(max_length=20, default=None, null=True)
    address = models.CharField(max_length=80)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    khoihoc = models.CharField(max_length=200, null=True, blank=True)
    diemchuyen = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    class Meta:
        ordering = ['-id']
    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.name + " " + self.khoihoc
