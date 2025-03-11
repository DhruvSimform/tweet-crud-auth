from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def index(request):

    return render(request,"index.html")

from django.shortcuts import render
from .models import Tweet

from django.shortcuts import render
from .models import Tweet

from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
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