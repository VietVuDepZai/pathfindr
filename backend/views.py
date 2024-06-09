from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404,HttpResponseRedirect
from backend.forms import *
from backend.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.filters import *
from django.http import JsonResponse
from .decorators import *
from django.utils.text import slugify
import urllib.parse
import google.generativeai as genai
genai.configure(api_key="AIzaSyBLccnrIBeX4QpflJE1lKbSLleiv-MA6YA")
def text_to_html_paragraphs(text):
    # First, replace multiple newlines with a single newline,
    # so you don't get empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)

    # Split the text into lines
    lines = text.split('\n')

    # Wrap each line in a <p> tag and join them
    return ''.join(f'{line.strip()}\n<br>' for line in lines)
def chat(request):   
    try: 
        student = Studenddt.objects.get(user=request.user)
    except:
        student = 'Nothing'
    return render(request, 'chat.html', {'student':student})
def chatgpt(request):
    text = request.GET.get('prompt')
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    chat = model.start_chat()
    response = chat.send_message(text)
    # Extract necessary data from response
    mess = text_to_html_paragraphs(response.text)
    return JsonResponse({"message":  mess})
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def signup(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/choosing')
    return render(request, 'signup.html', {'form': form})
# Create your views here.
def home(request):
    try: 
        student = Studenddt.objects.get(user=request.user)
    except:
        student = 'Nothing'
    return render(request, 'index.html', {'student':student})
def question(request):
    try: 
        student = Studenddt.objects.get(user=request.user)
    except:
        student = 'Nothing'
    return render(request, 'question.html', {'student':student})
def profile(request):
    student = Studenddt.objects.get(user=request.user)
    posts = Post.objects.exclude(headline=student.school)
    if request.method == 'POST':
        return redirect('/profile')

    return render(request, 'profile.html', {'student':student,'posts':posts})
def history(request):
    student = Studenddt.objects.get(user=request.user)
    result = Result.objects.filter(tester=student, khoihoc__isnull=False).order_by('-id')
    return render(request, 'history.html',{'result':result,'student':student})
def result(request): 
    diemTong = 0
    chuyenbool =  request.COOKIES.get("answer")
    tichhop =  request.COOKIES.get("tichhop")
    monchuyen = request.COOKIES.get("subject")
    diemToan = float(request.COOKIES.get("Toán") or 0)
    diemVan = float(request.COOKIES.get("Văn") or 0)
    diemAnh = float(request.COOKIES.get("Anh") or 0)
    diemChuyen = float(request.COOKIES.get(monchuyen) or 0)
    diemtichhop = float(request.COOKIES.get("tiếng Anh tích hợp") or 0)
    try: 
        diemToan = diemToan.replace(",",".")
        diemVan = diemVan.replace(",",".")
        diemAnh = diemAnh.replace(",",".")
        diemChuyen = diemChuyen.replace(",",".")
    except:
        pass
    try: 
        diemToan = diemToan.replace(",",".")
        diemVan = diemVan.replace(",",".")
        diemAnh = diemAnh.replace(",",".")
        diemtichhop = diemtichhop.replace(",",".")
    except:
        pass        
    if chuyenbool == 'yes':
        diemTong = float(diemToan) + float(diemVan) + float(diemAnh) + float(diemChuyen)*2
        if diemTong >= 20:
            thpt = XetDiemChuyen.objects.filter(khoihoc=monchuyen, diemchuyen__lte=diemTong).order_by('-diemchuyen')[:3]
            print(thpt)
        else: 
            return redirect('/path')
    if chuyenbool == 'no':
        if tichhop == 'yes':
            diemTong = float(diemToan) + float(diemVan) + float(diemAnh) + float(diemtichhop)
            print(diemTong)
            monchuyen = 'Tích hợp'
            if diemTong >= 20:
                thpt = XetDiemChuyen.objects.filter(khoihoc=monchuyen, diemchuyen__lte=diemTong).order_by('-diemchuyen')[:3]
                print(thpt)
            else: 
                return redirect('/path')
        elif tichhop == 'no':
            diemTong = float(diemToan) + float(diemVan) + float(diemAnh)
            monchuyen = 'Không chuyên'
            if diemTong >= 20:
                thpt = XetDiemChuyen.objects.filter(khoihoc="không chuyên", diemchuyen__lte=diemTong).order_by('-diemchuyen')[:3]
                print(thpt)
            else: 
                return redirect('/path')
    try: 
        student = Studenddt.objects.get(user=request.user)
        Result.objects.create(
            marks=diemTong,
            khoihoc=monchuyen,
            tester = student
            )
    except: 
        student = 'none'
        Result.objects.create(
            marks=diemTong,
            khoihoc=monchuyen,
            )

    return render(request, 'result.html', {'thpt':thpt,'student':student})
def resultpk(request, pk):
    student = Studenddt.objects.get(user=request.user)
    result = Result.objects.get(id=pk)
    thpt = XetDiemChuyen.objects.filter(khoihoc=result.khoihoc, diemchuyen__lte=result.marks).order_by('-diemchuyen')[:3]
    return render(request, 'resultpk.html', {'thpt':thpt,'student':student})
    
def path(request):
    try: 
        student = Studenddt.objects.get(user=request.user)
    except:
        student = 'Nothing'
    return render(request, 'score.html', {'student':student})
def listresult(request,id):
    tester = Studenddt.objects.get(id=id)
    result=Result.objects.filter(tester=tester)
    return render(request,'fine.html',{'result':result})
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/signin')
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        print("HSuuu")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print("HSuuu")
            auth_login(request, user)
            return redirect("/")
        

    context = {}
    return render(request, 'login.html', context)
def newforum(request):
	posts = DienDan.objects.all().order_by('-created')
	student = Studenddt.objects.get(user=request.user)
	if request.method == 'POST':
		DienDan.objects.create(
		    author=student,
		    body=request.POST['comment']
		    )
		return redirect('/forums')

	context = {'posts':posts,'student':student}
	return render(request, 'newforum.html', context)
def admincp(request):
    if request.user.is_superuser:
        return redirect("/adminmain")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            print("HSuuu")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_superuser:
                    return redirect("/adminmain")
                else:
                    return redirect("/logout")
        

    context = {}
    return render(request, 'admin/login.html', context)
@csrf_exempt
def post(request, name):
    name = urllib.parse.unquote(name)
    try:
        post = Post.objects.get(headline=name)
    except:
        post = Post.objects.get(slug=name)
    try:
        student = Studenddt.objects.get(user=request.user)
    except:
        student = ''

    comments = PostComment.objects.filter(post=post)
    commentscount = PostComment.objects.filter(post=post).count()

    if request.method == 'POST':
        student = Studenddt.objects.get(user=request.user)
        PostComment.objects.create(
            author=student,
            post=post,
            body=request.POST['comment']
            )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect(f'/post/{post.slug}')


    context = {'post':post, 'comments':comments, 'count':commentscount,'student':student}
    return render(request, 'post.html', context)

@csrf_exempt
def adminpost(request, name):
    try:
        post = Post.objects.get(id=name)
    except:
        post = Post.objects.get(slug=name)
    if request.method == 'POST':
        student = Studenddt.objects.get(user=request.user)
        PostComment.objects.create(
            author=student,
            post=post,
            body=request.POST['comment']
            )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('post', slug=post.slug)


    context = {'post':post}
    return render(request, 'admin/post.html', context)
def posts(request):
	try: 
		student = Studenddt.objects.get(user=request.user)
	except:
		student = 'dodob'
	posts = Post.objects.filter(featured=False).order_by('-created')
	myFilter = PostFilter(request.GET, queryset=posts)
	posts = myFilter.qs

	page = request.GET.get('page')

	paginator = Paginator(posts, 5)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'posts':posts, 'myFilter':myFilter,'student':student}
	return render(request, 'posts.html', context)
def forums(request):
    posts = DienDan.objects.all().order_by('-created')
    try: 
        student = Studenddt.objects.get(user=request.user)
        if request.method == 'POST':
            student = Studenddt.objects.get(user=request.user)
            post = DienDan.objects.get(id=request.POST['id_diendan'])
            DienDanComment.objects.create(
                author=student,
                post=post,
                body=request.POST['comment']
                )
            messages.success(request, "You're comment was successfuly posted!")

            return redirect(f'/forums')
        context = {'posts':posts,'student':student}
        return render(request, 'forums.html', context)
    except:
        context = {'posts':posts}
        return render(request, 'guest.html', context)
@admin_only
def addPost(request):
	form = PostForm()

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('/adminposts')

	context = {'form':form}
	return render(request, 'admin/postreal_form.html', context)
@admin_only
def addDienDan(request):
	form = DienDanForm()
	posts = DienDan.objects.all().order_by('-created')
	if request.method == 'POST':
		form = DienDanForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('/adminforums')

	context = {'form':form, 'posts':posts}
	return render(request, 'admin/addforum.html', context)
from django.db.models import Q

def chuyen(request):
    thpt = XetDiemChuyen.objects.exclude(Q(khoihoc='không chuyên') | Q(khoihoc='Tích hợp'))
    myFilter = THPTFilter(request.GET, queryset=thpt)
    thpt = myFilter.qs
    paginator = Paginator(thpt, 5)
    page = request.GET.get('page')
    try:
        thpt = paginator.page(page)
    except PageNotAnInteger:
        thpt = paginator.page(1)
    except EmptyPage:
        thpt = paginator.page(paginator.num_pages)

    return render(request, 'admin/chuyen.html', {'thpt': thpt, 'myFilter':myFilter})


def khongchuyen(request):
    thpt = XetDiemChuyen.objects.filter(khoihoc='không chuyên')
    myFilter = Nonfilter(request.GET, queryset=thpt)
    thpt = myFilter.qs
    paginator = Paginator(thpt, 5)
    page = request.GET.get('page')
    try:
        thpt = paginator.page(page)
    except PageNotAnInteger:
        thpt = paginator.page(1)
    except EmptyPage:
        thpt = paginator.page(paginator.num_pages)

    return render(request, 'admin/khongchuyen.html', {'thpt': thpt, 'myFilter':myFilter})
def tichop(request):
    thpt = XetDiemChuyen.objects.filter(khoihoc='Tích hợp')
    myFilter = Nonfilter(request.GET, queryset=thpt)
    thpt = myFilter.qs
    paginator = Paginator(thpt, 5)
    page = request.GET.get('page')
    try:
        thpt = paginator.page(page)
    except PageNotAnInteger:
        thpt = paginator.page(1)
    except EmptyPage:
        thpt = paginator.page(paginator.num_pages)

    return render(request, 'admin/tichop.html', {'thpt': thpt, 'myFilter':myFilter})
@admin_only
def createPost(request):
	form = XetDiemChuyenForm()

	if request.method == 'POST':
		form = XetDiemChuyenForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('/chuyen')

	context = {'form':form}
	return render(request, 'admin/post_form.html', context)
@admin_only
def updatePost(request, slug, red):
	post = XetDiemChuyen.objects.get(id=slug)
	form = XetDiemChuyenForm(instance=post)

	if request.method == 'POST':
		form = XetDiemChuyenForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
		return redirect(f'/{red}')

	context = {'form':form}
	return render(request, 'admin/post_form.html', context)
@admin_only
def updateRealPost(request, id):
	post = Post.objects.get(id=id)
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
		return redirect('/adminposts')

	context = {'form':form}
	return render(request, 'admin/postreal_form.html', context)
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        print("HSuuu")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print("HSuuu")
            auth_login(request, user)
            return HttpResponseRedirect('/')

        

    context = {}
    return render(request, 'signin.html', context)
def studentsignup(request):
    userForm=RegistrationForm()
    teacherForm=StudentForm()
    posts = Post.objects.all()
    mydict={'form':userForm,'StudentForm':teacherForm,'posts':posts}
    if request.method=='POST':
        userForm=RegistrationForm(request.POST)
        teacherForm=StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            userForm.save()
            teacher=teacherForm.save(commit=False)
            user = User.objects.get(username=request.POST.get('username'))
            teacher.user=user
            teacher.save()
        return HttpResponseRedirect('/signin')
    return render(request, 'studentregist.html', mydict)
def googlesignup(request,red):
    try:
        if red == 'home':
            red = ""
        student = Studenddt.objects.get(user=request.user)
        return redirect(f'/{red}')
    except:
        teacherForm=StudentForm()
        posts = Post.objects.all()
        mydict={'form':teacherForm,'posts':posts}
        if request.method=='POST':
            teacherForm=StudentForm(request.POST,request.FILES)
            if teacherForm.is_valid():
                teacher=teacherForm.save(commit=False)
                teacher.user=request.user
                teacher.save()
            return HttpResponseRedirect('/')
        return render(request, 'signup.html', mydict)
def adminposts(request):
	posts = Post.objects.filter().order_by('-created')
	myFilter = PostFilter(request.GET, queryset=posts)
	posts = myFilter.qs

	page = request.GET.get('page')

	paginator = Paginator(posts, 5)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'posts':posts, 'myFilter':myFilter}
	return render(request, 'admin/posts.html', context)
def adminforums(request):
    posts = DienDan.objects.all().order_by('-created')

    if request.method == 'POST':
        student = Studenddt.objects.get(user=request.user)
        post = DienDan.objects.get(id=request.POST['id_diendan'])
        DienDanComment.objects.create(
            author=student,
            post=post,
            body=request.POST['comment']
            )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect(f'/adminforums')
    context = {'posts':posts}
    return render(request, 'admin/forums.html', context)
def adminmain(request):
    chuyen = XetDiemChuyen.objects.exclude(Q(khoihoc='không chuyên') | Q(khoihoc='Tích hợp')).count()
    kochuyen = XetDiemChuyen.objects.filter(khoihoc='không chuyên').count()
    tichop = XetDiemChuyen.objects.filter(khoihoc='Tích hợp').count()
    posts = Post.objects.all().count()

    

    return render(request, 'admin/adminpanel.html', {'chuyen': chuyen, 'kochuyen':kochuyen,'tichop':tichop,'posts':posts})

