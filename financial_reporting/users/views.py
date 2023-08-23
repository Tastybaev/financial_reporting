from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import CreationForm, ProfileForm, CategoryForm
from .models import Profile
from finances.models import Category


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

@login_required
def update_profile(request):
    if request.method == 'POST':
        categoryform = CategoryForm(data=request.POST)
        if categoryform.is_valid():
            new_category = categoryform.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect('users:settings')
    else:
        categoryform = CategoryForm
    if request.method == 'POST':
        userform = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if userform.is_valid():
            userform.save()
            return redirect('users:settings')
    else:
        userform = ProfileForm(instance=request.user.profile)
    categories = Category.objects.filter(owner=request.user)
    context = {
        'userform': userform,
        'categoryform': categoryform,
        'categories': categories
    }
    return render(request, 'users/account/settings.html', context)

@login_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'message':'Категория не найдена!'})
    # Удалите транзакцию
    try:
        category.delete()
        return JsonResponse({'success': True, 'message':'Категория успешно удалена'})
    except ProtectedError:
        return JsonResponse({'success': False, 'message':'Нельзя удалить категорию у которой есть транзакции.'})

# Добавить стандартный набор категорий для всех пользователей.