from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
# Create your views here.

def index(request):
    return render(request,'chatroom/index.html')


@login_required
def room(request,room_name):
    return render(request,'chatroom/chat.html',{
        'room_name_json' : mark_safe(json.dumps(room_name)),
        'user': mark_safe(json.dumps(request.user.username))
    })
