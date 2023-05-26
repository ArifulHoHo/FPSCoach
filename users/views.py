from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, SkillForm, ProfileForm, CoachForm, ReviewForm, BookSessionForm, MessageForm, PostForm
from .models import Profile, NewsPortalPost, Tag, ValorantData
from django.db.models import Q
# Create your views here.


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile
    
    try:
        stats = profile.valorantdata
    except:
        stats = None
    skills = profile.skill_set.all()
    reviews = profile.reviews.all()
    
    context = {'profile':profile,'stats':stats,'skills':skills,'reviews':reviews}
    return render(request,'users/account.html',context)

def loginUser(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User successfully logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.error(request, 'An error has occured during registration!')

    context = {'page':page,'form':form}
    return render(request, 'users/login_register.html',context)


def coachPage(request): 

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    try:
        search_query = int(search_query)
        coaches = Profile.objects.distinct().filter(
        Q(is_coach = True) &
        (Q(name__icontains = search_query) |
        Q(username__icontains = search_query) |
        Q(coachprofile__session_price__lte = int(search_query)))
        )
    except:
        
        coaches = Profile.objects.distinct().filter(
        Q(is_coach = True) &
        (Q(name__icontains = search_query) |
        Q(username__icontains = search_query))
        )

        

    
    
    context={'coaches':coaches}
    return render(request,'users/index.html',context)

def showcoachProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    form = ReviewForm()

    try:
        stats = profile.valorantdata
    except:
        stats = None
    skills = profile.skill_set.all()
    reviews = profile.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print('valid')
            if profile.is_coach:
                review = form.save(commit=False)
                review.owner = request.user.profile
                review.coach = profile
                review.coachID = profile.coachprofile
                review.save()

                profile.coachprofile.getVoteCount

                messages.success(request,'Review Saved!')
                return redirect('coach-profile',pk)
            else:
                review = form.save(commit=False)
                review.owner = request.user.profile
                review.coach = profile
                
                review.save()
                messages.success(request,'Review Saved!')
                return redirect('coach-profile',pk)

    context = {'profile':profile,'stats':stats,'skills':skills,'reviews':reviews,'form':form}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added!')
            return redirect('account')

    context = {'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Change was saved!')
            return redirect('account')

    context = {'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def upgradeCoach(request):
    form = CoachForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            coachobj=form.save(commit=False)
            coachobj.coach = profile
            coachobj.save()
            profile.is_coach = 'True'
            profile.save()
            messages.success(request,'Change was saved!')
            return redirect('account')
        
    context = {'form':form}
    return render(request,'users/coach_form.html',context)


def requestUpgradeToCoach(request):
    OP_list = ['Immortal 3', 'Immortal 4','Radiant']
    profile = request.user.profile
    
    try:
        stats = profile.valorantdata
    except:
        stats = None
    if request.method == 'POST':
        if stats != 'None':
            if stats.peak_rank in OP_list:
                return redirect('new-coach-info')
                
            else:
                messages.error(request,'You are not eligible!')
        else:
            messages.error(request,'Connect valorant account first!')
        return redirect('account')
        

    return render(request,'users/upgrade-user.html')

@login_required(login_url='login')
def bookSession(request,pk):
    profile = Profile.objects.get(id=pk)
    form = BookSessionForm()
    if request.method == 'POST':
        form = BookSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            
            session.coachBooked = profile
            session.bookUser = request.user.profile
            session.session_price = profile.coachprofile.session_price
            session.save()
            return redirect('account')
    context = {'form':form,'profile':profile}
    return render(request,'users/book_form.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request,'users/message.html',context)

@login_required(login_url='login')
def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request,'Message sent!')
            return redirect('coach-profile',pk)

    context = {'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)

def showNotifications(request):
    profile = request.user.profile
    
    # try:
    #         sessions = profile.booksession.all()
            
    # except:
    #         sessions = profile.bookuser.all()
        
    sessions = profile.bookuser.all()
    if len(sessions) == 0:
        sessions = profile.booksession_set.all()
    print(sessions)
    context = {'sessions':sessions}
    return render(request,'users/notification.html',context)

def cancelSession(request,pk):
    profile = request.user.profile
    try:
        session = profile.bookuser.get(id=pk)
    except:
        session = profile.booksession_set.get(id=pk)

    if request.method == 'POST':
        session.delete()
        return redirect('notifications')
    
    context = {'session':session}
    return render(request,'users/cancelSession.html',context)

def showNews(request):

    
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains = search_query)

    news = NewsPortalPost.objects.distinct().filter(
        Q(title__icontains = search_query) |
        Q(description__icontains = search_query) |
        Q(creator__name__icontains = search_query) |
        Q(tags__in = tags)
    )

    context = {'news':news,'search_query':search_query}
    return render(request,'users/newsportal.html',context)

def showSinglePost(request,pk):
    post = NewsPortalPost.objects.get(id=pk)
    context = {'post':post}
    return render(request,'users/single-news.html',context)

@login_required(login_url='login')
def addPost(request):
    
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user.profile
            post.save()

            messages.success(request,'Post is published!')
            return redirect('news-portal')

    context = {'form':form}
    return render(request,'users/post_form.html',context)

