from django.shortcuts import render, redirect
from psiuChat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def chatHome(request):
    return render(request, 'chatHome.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.user.get_full_name()

    if Room.objects.filter(name=room).exists():
        return redirect('/psiuChat/'+room)
    else:
        new_room = Room.objects.create()
        new_room.save()
        return redirect('/psiuChat/'+room)

def send(request):
    message = request.POST['message']
    username = request.user.get_full_name()
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})