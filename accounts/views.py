from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/feed/')
        else:
            messages.error(request, "Invalid username or password")
    return render(request,'login.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username').strip().lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        agree = request.POST.get('agree')

        if not username or not password1 or not password2 or not agree:
            return render(request, 'register.html', {'error': 'All fields are required'})
        
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.full_name = full_name
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('/login')

    return render(request, 'register.html')

@never_cache
def logout_view(request):
    logout(request)
    return redirect('/login')

from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        profile.bio = request.POST.get('bio')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
        
    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def search_users(request):
    query = request.GET.get('q')
    profiles = []
    if query:
        # Search by username (icontains for case-insensitive partial match)
        profiles = Profile.objects.filter(user__username__icontains=query)
    
    return render(request, 'search.html', {'profiles': profiles, 'query': query})


def profile_detail(request, username):
    user_obj = get_object_or_404(User, username=username)

    profile, created = Profile.objects.get_or_create(user=user_obj)

    return render(request, 'profile_view.html', {
        'profile': profile,
        'user_obj': user_obj,
    })

@login_required
def inbox(request):
    conversations = request.user.conversations.all().order_by('-created_at')

    return render(request, 'chat/inbox.html', {
        'conversations': conversations
    })