from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import User_post

# Create your views here.
@login_required
@never_cache
def feed(request):
    posts = User_post.objects.all()
    return render(request, 'post.html', {'posts': posts})

@login_required
@never_cache
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if title and content:
            User_post.objects.create(
                user=request.user,
                title=title,
                content=content,
                photo=image
            )
        return redirect('feed')

        profile = request.user.profile
        return render(request, 'create_post.html', {
            'profile': profile
        })

            
    return render(request, 'create_post.html')