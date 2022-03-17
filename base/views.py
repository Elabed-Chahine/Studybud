from django.shortcuts import render
from django.http import HttpResponse


rooms = [
    {'id':1, 'name':'lets learn Python !'},
    {'id':2, 'name':'design with me !'},
    {'id':3, 'name':'Front end developers !'},
]


# Create your views here. render('home.html'); render('room.html');
def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html',context)


def room(request,pk):
    room = None
    for i in rooms:
        if i['id']==pk:
            room=i
    return render(request, "base/room.html",{'room':room})


    