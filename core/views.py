from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from .forms import SignUpForm,PasswordChangingForm,PrivacyForm,AddProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile
import uuid
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from friend.models import FriendRequest

def frontpage(request):
    return redirect("friends")

def login_user(request):
    if request.user.is_authenticated:
        return redirect('friends')
    else:
        if request.method == "POST":
            try:
                user = authenticate(request,username=User.objects.get(email=request.POST["email"]).username,password=request.POST["password"])
            except:
                messages.error(request,"Invalid Email or Password")
                return redirect("login")

            if user is not None:
                if user.is_superuser and Profile.objects.filter(user=user).exists() == False:
                    Profile.objects.create(user=user,verified=True)
                if Profile.objects.filter(user=user).exists():
                    if Profile.objects.get(user=user).verified:
                        login(request,user)
                        return redirect("friends")
                    else:
                        messages.success(request,f"Please activate your account!<a href=\'/send_verify_email/{user.id}/\'>click here</a>")
                        return redirect("login")
                else:
                    login(request, user)
                    return redirect("add-profile")
            else:
                messages.error(request,"Invalid Email or Password")
                return redirect("login")

        else:

            return render(request,"core/login.html",{"disable_navbar":True})

def signup(request):
    if request.user.is_authenticated:
        return redirect('friends')
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            email = request.POST["email"]
            if User.objects.filter(email=email).exists():
                messages.error(request,"This email already exists!")
                return redirect("signup")
            else:
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password1']
                    user = authenticate(request,username=username,password=password)
                    pr = Profile.objects.create(user=user,otp=str(uuid.uuid4()),activation_pass=password)
                    pr.friends.add(user)
                    return redirect("send-verify-email",pk=user.id)

        else:
            form = SignUpForm()

        return render(request,"core/signup.html",{
            "form":form,"disable_navbar":True
        })

def send_verify_email(request,pk):
    try:
        user = User.objects.get(id=pk)
        email_body = render_to_string("core/activationmail.html",{
            "user":user,
            "otp":Profile.objects.get(user=user,).otp,
            "domain":get_current_site(request)
        })
        send_mail(
            "Pinechat Email Verification",
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        return render(request,"core/send_verify_email.html",{"disable_navbar":True})
    except Exception as e:
        messages.error(request,"There was an error!Try to login!")
        print(e)
        return redirect("login")

def verify_email(request,otp):
    try:
        p = Profile.objects.get(otp=otp)
        user = authenticate(request, username=p.user.username, password=p.activation_pass)
        p.verified = True
        p.activation_pass = ""
        p.save()
        login(request,user)
        return render(request,"core/activation.html",{"disable_navbar":True})
    except:
        messages.error(request,"There was an error!Try to login!")
        return redirect("login")

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "User is deleted successfully!")
    return redirect("login")

@login_required
def privacy_settings(request):
    form = PrivacyForm(request.POST or None,instance=request.user)
    if request.method == "POST":
        email = request.POST["email"]
        if request.user.email != email and User.objects.filter(email=email).exists():
            messages.error(request,"This email allready exists")
            return redirect("privacy-settings")

    if form.is_valid():
        form.save()
        return redirect("friends")

    return render(request,"core/privacy_settings.html",{"form":form})

@login_required
def change_password(request):
    if SocialAccount.objects.filter(user=request.user).exists():
        messages.error(request,f"You are logged in with {SocialAccount.objects.get(user=request.user).provider}")
        return redirect("friends")
    else:
        if request.method == "POST":
            form = PasswordChangingForm(request.user,request.POST)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Password is changed successfully!")
                return redirect("friends")
            else:
                messages.error(request,"There was an error!")
                return redirect("change-password")

        else:
            form = PasswordChangingForm(request.user)
        
            return render(request,"core/change_password.html",{
                "form":form, 
            })

def profile(request,pk):
    if request.user.id == pk and Profile.objects.filter(user=User.objects.get(id=pk)).exists() == False:
        return redirect("add-profile")
    page_user = Profile.objects.get(user=User.objects.get(id=pk))
    context = {"page_user":page_user,}
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            frnds = Profile.objects.get(user=request.user).friends.all()
            req_sent = FriendRequest.objects.filter(sender=request.user,receiver=page_user.user).exists()
            req_rec = FriendRequest.objects.filter(sender=page_user.user,receiver=request.user).exists()
            context["frnds"] = frnds
            context["req_sent"] = req_sent
            context["req_rec"] = req_rec
        else:
            return redirect("add_profile")

    return render(request,"core/profile.html",context)

@login_required
def add_profile(request):
    if Profile.objects.filter(user=request.user).exists() == False:
        if request.method == "POST":
            form = AddProfileForm(request.POST,request.FILES)
            if form.is_valid():
                prof = form.save(commit=False)
                prof.user = request.user
                prof.friends.add(request.user)
                prof.save()
                return redirect("profile",pk=request.user.id)

        else:
            form = AddProfileForm
            return render(request,"core/add_profile.html",{
                "form":form
            })

    else:
        return redirect("profile",pk=request.user.id)

@login_required
def edit_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        me = Profile.objects.get(user=request.user)
        if request.method == "POST":
            form = AddProfileForm(request.POST or None,request.FILES or None,instance=me)
            if form.is_valid():
                form.save()
                return redirect("profile",pk=request.user.id)

        else:
            form = AddProfileForm
            return render(request,"core/edit_profile.html",{
                "form":form,
                "me":me
            })

    else:
        return redirect("add-profile",)

def handle404(request,exception):
    return render(request,'core/404.html',{})

def handle500(request):
    return render(request,'core/500.html',{})