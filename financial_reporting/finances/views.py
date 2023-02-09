from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,  render

from .models import Category, Transaction


def index(request):
    templates = 'finances/index.html'
    text = 'Это главная страница проекта financial_reporting'
    context = {
        'text': text,
    }
    return render(request, templates, context)


@login_required
def profile(request, User):
    user = get_object_or_404(User, user=User)
    context = {
        'user': user,
        'profile': user,
    }
    return render(request, "finances/profile.html", context)


# @login_required
def transaction_list(request):
    # user = get_object_or_404(User, user=User)
    transactions = Transaction.objects.all()
    context = {
        'transactions': transactions,
        # 'user': user,
    }
    return render(request, "finances/transactions.html", context)


# @login_required
# def transaction_create(request):
#     form = PostForm(request.POST or None, files=request.FILES or None)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         return redirect('posts:profile', username=request.user)
#     return render(request, 'posts/create_post.html', {'form': form})