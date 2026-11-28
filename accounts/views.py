from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from .decorators import role_required
from .models import User
from vocabulary.models import SavedWord, SearchLog, Word


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('accounts:login')
        messages.error(request, 'Please fix the errors below.')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_redirect(request):
    if request.user.role == User.ADMIN:
        return redirect('accounts:admin_dashboard')
    return redirect('accounts:member_dashboard')


@role_required(User.ADMIN)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_words': Word.objects.count(),
        'total_saved_words': SavedWord.objects.count(),
        'total_searches': SearchLog.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@role_required(User.MEMBER)
def member_dashboard(request):
    recent_saved = SavedWord.objects.filter(
        user=request.user
    ).select_related('word')[:5]
    return render(request, 'accounts/member_dashboard.html', {'recent_saved': recent_saved})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
        messages.error(request, 'Please fix the errors below.')
    return render(request, 'accounts/profile_edit.html', {'form': form})