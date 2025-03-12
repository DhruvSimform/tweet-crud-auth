from django.shortcuts import render
from .models import Tweet , Profile
from .forms import TweetForm , UserRegistrationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .neo_models import UserNode

# Create your views here.

def index(request):

    return render(request,"index.html")

from django.shortcuts import render
from .models import Tweet

from django.shortcuts import render
from .models import Tweet

from django.shortcuts import render
from .models import Tweet
from django.core.paginator import Paginator
from django.http import JsonResponse



def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')  # Order by latest
    query=request.GET.get('q', '')

    tweets = (tweets.filter(text__icontains=query) | tweets.filter(user__username__icontains=query)).order_by('-created_at')
    # Handle AJAX request for pagination
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        page_number = request.GET.get('page', 1)
        paginator = Paginator(tweets, 10)  # Show 5 tweets per page

        try:
            page = paginator.page(page_number)
        except:
            return JsonResponse({'tweets': []})  # No more tweets

        tweets_data = [
            {
                "id": tweet.id,
                "text": tweet.text,
                "username": tweet.user.username,
                "photo": tweet.photo.url if tweet.photo else None
            }
            for tweet in page.object_list
        ]
        return JsonResponse({'tweets': tweets_data})

    return render(request, "tweet_list.html", {'tweets': tweets[:30]})  # Load first 5 initially




@login_required
def my_tweets(request):
    query = request.GET.get('q') or ''
    tweets = (Tweet.objects.filter(user=request.user) & Tweet.objects.filter(text__icontains=query)).order_by('-created_at')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        paginator = Paginator(tweets, 10)

        try:
            page = paginator.page(page_number)
        except:
            return JsonResponse({'tweets': []})
        
        tweets_data = [
            {
                "id": tweet.id,
                "text": tweet.text,
                "username": tweet.user.username,
                "photo": tweet.photo.url if tweet.photo else None
            }
            for tweet in page.object_list
        ]
        return JsonResponse({'tweets': tweets_data})
    return render(request, "tweet_list.html", {'tweets': tweets[:30]})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, 'Tweet created successfully')
            return redirect('tweet_list')
        else:
            messages.error(request, 'Error creating tweet')
            pass
    else:
        form = TweetForm()
    return render(request , "tweet_form.html", {'form': form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet updated successfully")
            return redirect('tweet_list')
        
    else:
        form = TweetForm(instance=tweet)
        
    return render(request, "tweet_form.html", {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        messages.success(request, "Tweet deleted successfully")
        return redirect('tweet_list')
    return render(request,"tweet_confirm_delete.html", {'tweet': tweet})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            login(request,user)
            messages.success(request, "Registration successful")
            messages.success(request, "Welcome to TweetApp , you are now logged in")
            next_url = request.GET.get('next') or request.POST.get('next') or 'tweet_list'  # Default to home if next is missing
            return redirect(next_url)
 

    else:
        form = UserRegistrationForm()
    return render(request,"registration/register.html", {'form': form})    


from django.shortcuts import render, get_object_or_404
from .models import Profile
from .neo_models import UserNode  # Assuming your Neo4j models are in neo_models.py

@login_required
def profile_view(request, username):
    # Fetch user from SQLite
    user = User.objects.filter(username=username).first()
    user_profile, created = Profile.objects.get_or_create(user=user)

    # Fetch user node from Neo4j
    try:
        user_node = UserNode.nodes.get(username=username)
    except UserNode.DoesNotExist:
        user_node = None

    # Initialize follow-related variables (Keeping your original logic)
    followers_count = len(user_node.followers.all()) if user_node else 0
    following_count = len(user_node.following.all()) if user_node else 0
    is_following = False

    if request.user.is_authenticated:
        try:
            current_user_node = UserNode.nodes.get(username=request.user.username)
            is_following = current_user_node.following.is_connected(user_node) if user_node else False
        except UserNode.DoesNotExist:
            is_following = False

    # Handle profile update only if the logged-in user owns the profile
    if request.user == user:
        if request.method == "POST":
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect("profile", username=request.user.username)  # Prevent form resubmission
        else:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=user_profile)
    else:
        user_form = None
        profile_form = None

    context = {
        "userr": user,
        "user_profile": user_profile,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_owner": request.user == user,
        "is_following": is_following,
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "profile.html", context)

from neomodel import DoesNotExist
def follow_user(request, username):
    """Allow the logged-in user to follow another user and refresh the profile page."""
    try:
        logged_in_user = UserNode.nodes.get(username=request.user.username)
        target_user = UserNode.nodes.get(username=username)

        # Use 'following' (not 'follows') as defined in the model
        if not logged_in_user.following.is_connected(target_user):
            logged_in_user.following.connect(target_user)
        else:
            logged_in_user.following.disconnect(target_user)  # Unfollow

    except DoesNotExist:
        pass  # Ignore if the user does not exist

    return redirect('profile', username=username)  # Reload the profile page