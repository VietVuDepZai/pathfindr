"""
URL configuration for huongnghiep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from backend import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/', views.login),
        path('forums/', views.forums),
                path('profile/', views.profile),
path('resultpk/<pk>',views.resultpk),
        path('adminforums/', views.adminforums),
                path('addDienDan/', views.addDienDan),
                                path('history/', views.history),

                path('newforum/', views.newforum),
path('googlesignup/<red>',views.googlesignup),

        path('admincp/', views.admincp),
                path('admincp/', views.admincp),
                path('adminmain/', views.adminmain),
                path('chuyen/', views.chuyen),
                                path('tichop/', views.tichop),

                path('khongchuyen/', views.khongchuyen),
                path('addthpt/', views.createPost),
                                path('updatethpt/<slug>/<red>', views.updatePost),

        path('ckeditor/', include('ckeditor_uploader.urls')),
            path('register',views.register,name="register"),
                        path('signin',views.signin,name="signin"),

   path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path("accounts/", include("allauth.urls")), #most important

            path('posts',views.posts,name="posts"),
            path('adminposts',views.adminposts,name="adminposts"),
                        path('addposts',views.addPost,name="addposts"),
    path('chatgpt/', views.chatgpt),
        path('chat/',views.chat,name="chat"),

path('updatePost/<id>',views.updateRealPost),
            path('signup',views.studentsignup,name="signup"),
            path('question',views.question,name="question"),
            path('result',views.result,name="result"),
            path('path',views.path,name="path"),
            path('post/<name>',views.post,name="post"),
            path('adminpost/<name>',views.adminpost,name="adminpost"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

