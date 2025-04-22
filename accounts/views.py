from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.db import models

from .forms import RegisterForm, AdForm
from ads.models import Ad, ExchangeProposal

User = get_user_model()

@login_required
def account_view(request):
    received_proposals = ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    ).order_by('-created_at')

    sent_proposals = ExchangeProposal.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    history_proposals = ExchangeProposal.objects.filter(
        models.Q(sender=request.user) | models.Q(ad_receiver__user=request.user),
        ~models.Q(condition='pending')
    ).order_by('-created_at')

    user_ads = Ad.objects.filter(user=request.user)

    context = {
        'received_proposals': received_proposals,
        'sent_proposals': sent_proposals,
        'history_proposals': history_proposals,
        'user_ads': user_ads,
    }
    return render(request, 'account.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ads')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ads')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('login')


class AdUpdateView(UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ad_form.html'

    def get_success_url(self):
        return reverse('account')


class AdDeleteView(DeleteView):
    model = Ad
    template_name = 'ad_confirm_delete.html'

    def get_success_url(self):
        return reverse('account')
