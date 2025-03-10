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

def tweet_list(request):
    query = request.GET.get('q') or ''
    suggestions = []
    if query:
        tweets = Tweet.objects.filter(text__icontains=query)| Tweet.objects.filter(user__username__icontains=query)
        suggestions = tweets.values_list("text", flat=True)  # Extract only text
        print(suggestions)
    else:
        tweets = Tweet.objects.all() 
    return render(request, 'tweet_list.html', {'tweets': tweets ,"suggestions": suggestions})

def my_tweets(request):
    query = request.GET.get('q') or ''
    tweets = Tweet.objects.filter(user=request.user) & Tweet.objects.filter(text__icontains=query)
    return render(request, 'tweet_list.html', {'tweets': tweets,})

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