from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Room,Message,Invite
from .forms import CreateRoom
from django.contrib import messages
from django.contrib.auth.models import User
import uuid

@login_required
def rooms(request):
    if request.user.is_superuser:
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(members=request.user)

    return render(request,"room/rooms.html",{
        "rooms": rooms
    })

@login_required
def room(request,pk):
    room = Room.objects.get(uuid=pk)
    members = room.members.all()
    messages = Message.objects.filter(room=room)#[0:25]

    return render(request,"room/room.html",{
        "room":room,
        "messages":messages,
        'members':members,
		'allowed':request.user in members,
		"rooms":Room.objects.filter(members=request.user)
    })

@login_required
def delete_room(request,pk):
	room = Room.objects.get(uuid=pk)
	if request.user.is_superuser or request.user.id == room.owner.id:
		room.delete()
		messages.success(request,"Room is deleted successfully")
	else:
		messages.error(request,"You are not allowed")
	return redirect("rooms")

@login_required
def leave_room(request,pk,userid):
	room = Room.objects.get(uuid=pk)
	owner = room.owner
	
	target = User.objects.get(id=userid)

	if target in room.members.all():
		if request.user.is_superuser or request.user.id == owner.id or request.user.id == target.id:
			room.members.remove(target)
		else:
			messages.error(request,"You are not allowed")
	else:
		messages.error(request,"There is an error")
	return redirect("rooms")

@login_required
def create_room(request):
	if request.method == "POST":
		form = CreateRoom(request.POST)

		if form.is_valid():
			if request.POST["password"] == request.POST["password2"]:
				room = form.save(commit=False)
				room.owner=request.user
				room.uuid = str(uuid.uuid4())
				room.save()
				room.members.add(request.user)
				return redirect("room",pk=room.uuid)
			else:
				messages.error(request,"Passwords are not same!")
				return redirect("create-room")

	else:
		form = CreateRoom
	
	return render(request,"room/create_room.html",{"form":form})

@login_required
def join_room(request):
	if request.method == "POST":
		try:
			room_uuid = request.POST["room_id"]
			room = Room.objects.get(uuid=room_uuid)
		except:
			messages.error(request,"Invalid Room ID!")
			return redirect("join-room")

		if room.password == request.POST["password"]:
			if request.user in room.members.all():
				messages.error(request,"You have already joined that room")
				return redirect("room",pk=room.uuid)
			else:
				room.members.add(request.user)
				return redirect("room",pk=room.uuid)
			
		else:
			messages.error(request,"Invalid Password!")
			return redirect("join-room")

	else:
		return render(request,"room/join_room.html",{})

@login_required
def edit_room(request,pk):
	room = Room.objects.get(uuid=pk)

	if request.user in room.members.all():
		form = CreateRoom(request.POST or None,instance=room)

		if form.is_valid():
			form.save()
			return redirect("room",pk=pk)
		
		return render(request,"room/edit_room.html",{
			"form":form,
			"room":room
		})
	else:
		messages.error(request,"You are not allowed")
		return redirect("rooms")

@login_required
def invite(request,pk):
	room = Room.objects.get(uuid=pk)
	if request.user in room.members.all():
		if request.method == "POST":
			try:
				email = request.POST["email"]
				user = User.objects.get(email=email)
			except:
				try:
					username = request.POST["username"]
					user = User.objects.get(username=username)
				except:
					messages.error(request,"There is an error!")
					return redirect("invite",pk=pk)

			if user.id != request.user.id:
				if user in room.members.all():
					messages.error(request,"Already in the room!")
					return redirect("invite",pk=pk)
				else:
					if Invite.objects.filter(reciever=user).exists():
						messages.error(request,"Already invited!")
						return redirect("invite",pk=pk)
					else:
						Invite.objects.create(room=room,sender=request.user,reciever=user)
						return redirect("room",pk=pk)
			else:
				messages.error(request,"There is an error!")
				return redirect("invite",pk=pk)

		else:
			return render(request,"room/invite.html",{})
	
	else:
		messages.error(request,"You are not allowed")
		return redirect("rooms")

@login_required
def invitations(request):
	invitations = Invite.objects.filter(reciever_id=request.user.id)[::-1]
	return render(request,"room/invitations.html",{"invitations":invitations})

@login_required
def accept_invite(request,pk):
	invitation = Invite.objects.get(id=pk)
	room = invitation.room
	if request.user.id == invitation.reciever.id:
		room.members.add(request.user)
		invitation.delete()
		return redirect("room",pk=room.uuid)

	else:
		messages.error(request,"You are not allowed")
		return redirect("rooms")

@login_required
def decline_invite(request,pk):
	invitation = Invite.objects.get(id=pk)
	if request.user.id == invitation.reciever.id:
		invitation.delete()
		messages.success(request,"Invitation is declined successfully!")
		return redirect("rooms")
	else:
		messages.error(request,"You are not allowed")
		return redirect("rooms")

@login_required
def delete_message(request,pk):
	message = Message.objects.get(id=pk)
	room = message.room.uuid
	if message.user == request.user:
		message.delete()
	return redirect("room",pk=room)

@login_required
def forward_message(request,roomid,messageid):
	room = Room.objects.get(uuid=roomid)
	message = Message.objects.get(id=messageid)

	Message.objects.create(room=room,user=request.user,content=message.content)
	return redirect("room",pk=room.uuid)