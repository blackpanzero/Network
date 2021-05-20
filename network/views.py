from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post, Profile, Like,Pic

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='')

def index(request):

    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        follower = Profile.objects.filter(target=request.user)
        following = Profile.objects.filter(follower=request.user)
        posts = Post.objects.filter(user=request.user).order_by('id').reverse()
        totalfollower = len(follower)
        totalfollowing = len(following)
        posts=posts.count()
        allusers=User.objects.all()

        fol=[]
        notfollowing=[]
        
        for u in following:
            fol.append(u.target)
           
        for a in allusers:
            if a not in fol and a != request.user :
                notfollowing.append(a)
     

    
      

    except TypeError:
        return render(request, "network/index.html", {'page_obj': page_obj})
 

    
    
    return render(request, "network/index.html", {'page_obj': page_obj,
    "non_followers":notfollowing,
     "current_totalfollower":totalfollower,"current_totalfollowing":totalfollowing,"current_posts":posts,
     "photo":Pic.objects.get(user=request.user)})
   
  



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        photo=request.POST["photo"]
        if photo=="":
            photo="https://i.stack.imgur.com/34AD2.jpg"

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "messages": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            photo=Pic(user=user,photolink=photo)
            photo.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "messages": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def profile(request, username):
    current_follower = Profile.objects.filter(target=request.user)
    current_following = Profile.objects.filter(follower=request.user)
    current_posts = Post.objects.filter(user=request.user).order_by('id').reverse()
    current_totalfollower = len(current_follower)
    current_totalfollowing = len(current_following)
    current_posts=current_posts.count()
    allusers=User.objects.all()

    fol=[]
    notfollowing=[]
    for u in current_following:
        fol.append(u.target)
    for a in allusers:
        if a not in fol and a != request.user :
            notfollowing.append(a)
     

    
    if request.method == 'GET':
        currentuser = request.user
        profileuser = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=profileuser).order_by('id').reverse()
        follower = Profile.objects.filter(target=profileuser)
        following = Profile.objects.filter(follower=profileuser)
        
        
        following_each_other = Profile.objects.filter(follower=currentuser, target=profileuser)
        totalfollower = len(follower)
        totalfollowing = len(following)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        current_follower = Profile.objects.filter(target=request.user)
        current_following = Profile.objects.filter(follower=request.user)
        current_posts = Post.objects.filter(user=request.user).order_by('id').reverse()
        current_totalfollower = len(current_follower)
        current_totalfollowing = len(current_following)
        current_posts=current_posts.count()
    
        

        return render(request, "network/profile.html", {'posts': posts.count(), 'profileuser': profileuser,
            'page_obj': page_obj, 'follower': follower, 'totalfollower':totalfollower, 'following': following, 'totalfollowing': totalfollowing,
            'followingEachOther': following_each_other,'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, 
            "photo":Pic.objects.get(user=request.user),"profile_photo":Pic.objects.get(user=profileuser),
            "non_followers":notfollowing})
        
    else:
        currentuser = request.user
        profileuser = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=profileuser).order_by('id').reverse()
        following_each_other = Profile.objects.filter(follower=request.user, target=profileuser)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if not following_each_other:
            follow = Profile.objects.create(target=profileuser, follower=currentuser)
            follow.save()
            follower = Profile.objects.filter(target=profileuser)
            following = Profile.objects.filter(follower=profileuser)
            following_each_other = Profile.objects.filter(follower=request.user, target=profileuser)
            totalfollower = len(follower)
            totalfollowing = len(following)

            return render(request, "network/profile.html", {'posts': posts.count(), 'profileuser': profileuser, 
            'page_obj': page_obj, 'follower': follower, 'following': following,
            'totalfollowing': totalfollowing, 'totalfollower': totalfollower,
            'followingEachOther': following_each_other,'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, "photo":Pic.objects.get(user=request.user),
            "profile_photo":Pic.objects.get(user=profileuser),"non_followers":notfollowing})

        else:
            following_each_other.delete()
            follower = Profile.objects.filter(target=profileuser)
            following = Profile.objects.filter(follower=profileuser)
            totalfollower = len(follower)
            totalfollowing = len(following)
       
            return render(request, "network/profile.html", {'posts': posts.count(), 'profileuser': profileuser, 
            'page_obj': page_obj, 'follower': follower, 'following': following, 
            'totalfollowing': totalfollowing, 'totalfollower': totalfollower,
            'followingEachOther': following_each_other,'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, "photo":Pic.objects.get(user=request.user),
            "profile_photo":Pic.objects.get(user=profileuser),"non_followers":notfollowing})

@login_required(login_url='login')
def newpost(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        return render(request, "network/newpost.html", {'user':user})
    else:
        user = get_object_or_404(User, username=username)
        textarea = request.POST["textarea"]
        post = Post.objects.create(content=textarea, user=user)
        post.save()
        return redirect("index")

@login_required(login_url='login')
def following(request, username):
    current_follower = Profile.objects.filter(target=request.user)
    current_following = Profile.objects.filter(follower=request.user)
    current_posts = Post.objects.filter(user=request.user).order_by('id').reverse()
    current_totalfollower = len(current_follower)
    current_totalfollowing = len(current_following)
    current_posts=current_posts.count()

    allusers=User.objects.all()
    fol=[]
    notfollowing=[]
    for u in current_following:
        fol.append(u.target)
    for a in allusers:
        if a not in fol and a != request.user :
            notfollowing.append(a)
     
    if request.method == 'GET':
        currentuser = get_object_or_404(User, username=username)
        follows = Profile.objects.filter(follower=currentuser)
        posts = Post.objects.all().order_by('id').reverse()
        posted = []
        for p in posts:
            for follower in follows:
                if follower.target == p.user:
                    posted.append(p)
        
        if not follows:
            return render(request, 'network/following.html', {'message': "You don't follow anybody",'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, "photo":Pic.objects.get(user=request.user),
            "non_followers":notfollowing})

        paginator = Paginator(posted, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'network/following.html', {'page_obj':page_obj,'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, "photo":Pic.objects.get(user=request.user),
             "non_followers":notfollowing})



@login_required(login_url='login')
def like_post(request):
    user = request.user
    if request.method == 'GET':
        post_id = request.GET['post_id']
        likedpost = Post.objects.get(pk=post_id)
        if user in likedpost.liked.all():
            likedpost.liked.remove(user)
            like = Like.objects.get(post=likedpost, user=user)
            like.delete()
        else:
            like = Like.objects.get_or_create(post=likedpost, user=user)
            likedpost.liked.add(user)
            likedpost.save()
        
        return HttpResponse('Success')

@login_required(login_url='login')
def config(request, username):
    current_follower = Profile.objects.filter(target=request.user)
    current_following = Profile.objects.filter(follower=request.user)
    current_posts = Post.objects.filter(user=request.user).order_by('id').reverse()
    current_totalfollower = len(current_follower)
    current_totalfollowing = len(current_following)
    current_posts=current_posts.count()
    user = request.user

    allusers=User.objects.all()
    fol=[]
    notfollowing=[]
    for u in current_following:
        fol.append(u.target)
    for a in allusers:
        if a not in fol and a != request.user :
            notfollowing.append(a)

    if request.method == 'GET':
        profile = User.objects.get(username=username)
        if request.user.is_anonymous:
            return redirect("login")
        if profile.username == user.username:
            return render(request, "network/config.html", {'profile': profile,'current_totalfollower':current_totalfollower,
            'current_totalfollowing': current_totalfollowing,'current_posts':current_posts, "photo":Pic.objects.get(user=request.user),
            "non_followers":notfollowing})
        else:
            return redirect("index")
        

    else: 
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        photo=request.POST["photo"]
        if photo=="":
            photo="https://i.stack.imgur.com/34AD2.jpg"

        pic=Pic.objects.get(user=request.user)
       
        pic.photolink=photo
        pic.save()

        profile = User.objects.get(username=username)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.email = email
        profile.save()
        return redirect('profile', profile.username)

def posts(request):
    # Return posts in reverse chronologial order
    posts=Post.objects.filter(user=request.user).all()
    posts = posts.order_by("-date").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
def tweet(request,post_id):
 
    user=request.user
     # Query for requested email

    try:
        tweet = Post.objects.get(pk=post_id)
        
    except Post.DoesNotExist:
        return JsonResponse({"error": "Tweet not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        if user in tweet.liked.all():
            tweet.liked.remove(user)
            like = Like.objects.get(tweet_id=tweet, user_id=user)
            like.delete()
        else:
            like = Like.objects.get_or_create(post=tweet, user=user)
            tweet.liked.add(user)
            tweet.save()
        

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)





@csrf_exempt
@login_required(login_url='login')
def editor(request,post_id):
    post = Post.objects.get(pk=post_id)
    
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    #post.content = data.get("body","")
    #post.save()
    print(data.get("body",""))

    post.content =data.get("body","")
    post.save()
         


    return JsonResponse({"message": "Tweet edited successfully."}, status=201)