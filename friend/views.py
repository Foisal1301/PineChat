from django.shortcuts import render,redirect
from .models import FriendRequest, MessageWithFriend
from core.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import json,re
from django.http.response import JsonResponse
from django.contrib import messages

def urlify(text):
    urls = re.findall(r'(https?://[^\s]+)', text)
    if len(urls) != 0:
        for i in urls:
            replaced = '<a target=\"_blank\" href=\"'+i+'\">'+i+'</a>'
            el = text.replace(i,replaced)
        return el
    return text

@login_required
def friends(request):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		friends = Profile.objects.get(user=request.user).friends.all()

		return render(request,'friend/friends.html',{
			'friends':friends
			})

@login_required
def friend(request,pk):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		friends = Profile.objects.get(user=request.user).friends.all()
		other_user = User.objects.get(pk=pk)
		if other_user in friends:
			messagess = MessageWithFriend.objects.filter(Q(receiver=request.user, sender=other_user))
			messagess.update(seen=True)
			messagess = messagess | MessageWithFriend.objects.filter(Q(receiver=other_user,sender=request.user))
			return render(request,"friend/friend_chat.html",{
				"other_user":other_user,
				"messages":messagess,
				"friends":friends,
				"own":request.user.id == other_user.id
				})
		else:
			return redirect("friends")

@login_required
def friend_ajax(request,pk):
	other_user = User.objects.get(id=pk)
	if request.user.id == other_user.id:
		message_list = []
	else:
		messagess = MessageWithFriend.objects.filter(seen=False,receiver=request.user)

		message_list = []
		for message in messagess:
			context = {
				"sender":message.sender.username,
				"message":message.message,
				"id":message.id,
				"sent":message.sender == request.user,
				'file':message.is_file
			}
			if message.is_file['ftype'] != None:
				context['url'] = message.file.url
			message_list += context


		message_list = [{
		"sender":message.sender.username,
		"message":message.message,
		"id":message.id,
		"sent":message.sender == request.user,
		'file':message.is_file
		} for message in messagess]
		
		messagess.update(seen=True)
	if request.method == "POST":
		message = json.loads(request.body)
		m = MessageWithFriend.objects.create(receiver=other_user,sender=request.user,message=urlify(message))
		message_list.append({
			"sender":request.user.username,
			"message":m.message,
			"id":m.id,
			"sent":True,
			})
	return JsonResponse(message_list,safe=False)

@login_required
def delete_message_frnd(request,pk):
	message = MessageWithFriend.objects.get(id=pk)
	if request.user == message.sender:
		message.delete()
		return redirect("friend",pk=message.receiver.id)

	elif request.user.is_superuser:
		message.delete()
		if message.sender != request.user:
			return redirect("friend",pk=message.sender.id)
		return redirect("friend",pk=message.receiver.id)

	else:
		return redirect("friend",pk=message.sender.id)

@login_required
def forward_message_frnd(request,userid,messageid):
	receiver = User.objects.get(id=userid)
	message = MessageWithFriend.objects.get(id=messageid)

	MessageWithFriend.objects.create(sender=request.user,receiver=receiver,message=message.message)
	return redirect("friend",pk=receiver.id)

@login_required
def unfriend(request,pk):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		frnd = User.objects.get(id=pk)
		if request.user in Profile.objects.get(user=frnd).friends.all() and frnd in Profile.objects.get(user=request.user).friends.all():
			Profile.objects.get(user=frnd).friends.remove(request.user)
			Profile.objects.get(user=request.user).friends.remove(frnd)

		return redirect("friends")

@login_required
def add_friend(request,pk):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		myfriends = Profile.objects.get(user=request.user).friends
		guest = User.objects.get(id=pk)
		if guest not in myfriends.all():
			if FriendRequest.objects.filter(receiver=guest).exists() == False:
				FriendRequest.objects.create(sender=request.user,receiver=guest)
				return redirect("friends")
			else:
				messages.error(request,"Already requested!")
				return redirect("friends")
		else:
			messages.error(request, "Already friend!")
			return redirect("friends")

@login_required
def accept_frndreq(request,pk):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		req = FriendRequest.objects.get(sender=User.objects.get(id=pk),receiver=request.user)
		if request.user == req.receiver or request.user.is_superuser:
			Profile.objects.get(user=req.sender).friends.add(request.user)
			Profile.objects.get(user=request.user).friends.add(req.sender)
			sender_id = req.sender.id
			req.delete()
			return redirect("friend",pk=sender_id)

		else:
			messages.error(request,"You are not allowed")
			return redirect("friends")

@login_required
def decline_frndreq(request,pk):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		req = FriendRequest.objects.get(sender=User.objects.get(id=pk),receiver=request.user)
		if request.user == req.receiver or request.user.is_superuser:
			req.delete()
			messages.success(request,"Request is declined successfully!")
			return redirect("friends")
		else:
			messages.error(request, "You are not allowed")
			return redirect("friends")

@login_required
def frnd_reqs(request):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		reqs = FriendRequest.objects.filter(receiver=request.user)
		return render(request,"friend/requests.html",{
			"reqs":reqs,
			"length":len(reqs)
		})
@login_required
def search(request):
	if Profile.objects.filter(user=request.user).exists() == False:
		return redirect("add-profile")
	else:
		if request.method == 'POST':
			searched = request.POST['searched']
			sort_by = request.POST['sort-by']
			if sort_by == "First Name":
				users = User.objects.filter(first_name__contains=searched)
			elif sort_by == "Last Name":
				users = User.objects.filter(last_name__contains=searched)
			elif sort_by == "Email":
				users = User.objects.filter(email__contains=searched)
			else:
				users = User.objects.filter(username__contains=searched)
			frnds = Profile.objects.get(user=request.user).friends.all()
			sent_req = []
			rec_req = []
			for i in FriendRequest.objects.filter(sender=request.user):
				sent_req.append(i.receiver)
			for i in FriendRequest.objects.filter(receiver=request.user):
				rec_req.append(i.sender)
			return render(request, 'friend/search.html', {
				'searched': searched,
				"users":users,
				'frnds':frnds,
				"sent_req":sent_req,
				"rec_req":rec_req,
				"len" : len(users) != 0
			})

@login_required
def cancel_friendreq(request,pk):
	req = FriendRequest.objects.get(sender=request.user,receiver=User.objects.get(id=pk))
	if request.user == req.sender:
		req.delete()
		messages.success(request,"Request is cancelled successfully!")
		return redirect("friends")
	else:
		messages.error(request,"You are not allowed")
		return redirect("friends")

def search_ajax(request):
	search = request.GET.get("q")
	sort_by = request.GET.get("sort-by")
	if sort_by == "First Name":
		objs = User.objects.filter(first_name__contains=search)
	elif sort_by == "Last Name":
		objs = User.objects.filter(last_name__contains=search)
	elif sort_by == "Email":
		objs = User.objects.filter(email__contains=search)
	else:
		objs = User.objects.filter(username__contains="Ad")

	results = []

	if search:
		for obj in objs:
			results.append({
				'username':obj.username
			})
	
	return JsonResponse({
		'status':True,
		'results':results
	})

@login_required
def uploadFile(request,pk):
	receiver=User.objects.get(id=pk)
	if request.method == "POST":
		try:
			files = request.FILES.getlist('file')
			for i in files:
				MessageWithFriend.objects.create(sender=request.user,receiver=receiver,file=i)
		except:
			messages.error(request,'File Uploading has been failed,try again!')
	return redirect(friend,pk)