
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm,UserForm

""" rooms = [
    {'id':1, 'name':'lets learn Python !'},
    {'id':2, 'name':'design with me !'},
    {'id':3, 'name':'Front end developers !'},
    el password ta3 admin django123456
] """

"""    form = RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host = request.user
            room.save() """

# Create your views here. render('home.html'); render('room.html');
def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None  else ''
    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) 

                                 ) 
    topics = Topic.objects.all()
    count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'topics': topics, 'rooms': rooms,'count':count,'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages= room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == 'POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, "base/room.html", context)

@login_required(login_url='/user_login')
def create_room(request):
    topics = Topic.objects.all()
    context = {'form': RoomForm,'topics': topics}

    if request.method == 'POST':
        topic_name =request.POST.get('topic')
        topic,created= Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')


     
        

    return render(request, "base/room_form.html", context)


@login_required(login_url='/user_login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed to update this')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')

        room.save()

        return redirect("home")
    context = {'form': form,'topics': topics,'room': room}
    return render(request, "base/room_form.html", context)


@login_required(login_url='/user_login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed to update this')
    if request.method == 'POST':
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {'room': room})

def login_user(request):
    page= 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'User OR Password does not exist.')
    context = {"page":page}
    return render(request, "base/login_user.html",context)



def logoutUser(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = UserCreationForm;
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:

            messages.error(request,"an error happened during registration")

    return render(request,"base/login_user.html",{'form': form})


@login_required(login_url='/user_login')
def deleteComment(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed to update this')
    if request.method == 'POST':
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {'room': room})


def userProfile(request, pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    count=rooms.count()
    messages= user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'topics':topics,'room_messages':messages,'count':count }
    return render(request,'base/profile.html',context)



def update_user(request):
    form= UserForm(instance=request.user)
    context= {'form':form}
    if request.method == 'POST':
        form=UserForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=request.user.id)

    return render(request, "base/update_user.html",context)