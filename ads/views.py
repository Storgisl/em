from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import Ad, ExchangeProposal
from .forms import ExchangeProposalForm, AdEditForm, AdCreateForm
from .basefolder.choices import CategoryChoices

def index(request):
    return render(request, "index.html")


@login_required
def ads_view(request):
    ads = Ad.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        ads = ads.exclude(user=request.user)

    category_filter = request.GET.get('category', '')
    if category_filter:
        ads = ads.filter(category=category_filter)

    context = {
        'ads': ads,
        'categories': CategoryChoices.choices(),
        'user_has_ads': Ad.objects.filter(user=request.user).exists() if request.user.is_authenticated else False,
        'user_ads_count': Ad.objects.filter(user=request.user).count() if request.user.is_authenticated else 0,
        'selected_category': category_filter
    }
    return render(request, 'ads.html', context)


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_ads'] = Ad.objects.filter(user=self.request.user).exists()
        return context


@login_required
def send_exchange_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)

    if ad_receiver.user == request.user:
        messages.error(request, "You cannot send an exchange proposal for your own ad.")
        return redirect('ad_detail', pk=ad_receiver.id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                existing = ExchangeProposal.objects.filter(
                    ad_sender=form.cleaned_data['ad_sender'],
                    ad_receiver=ad_receiver,
                    condition='pending'
                ).exists()

                if existing:
                    messages.warning(request, 'You already have a pending exchange proposal for this ad.')
                else:
                    proposal = form.save(commit=False)
                    proposal.ad_receiver = ad_receiver
                    proposal.sender = request.user
                    proposal.condition = 'pending'
                    proposal.save()
                    messages.success(request, 'Exchange proposal sent successfully!')
                    return redirect('ad_detail', pk=ad_receiver.id)

            except IntegrityError:
                messages.error(request, 'An error occurred while processing your proposal.')
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'exchange.html', {
        'form': form,
        'ad_receiver': ad_receiver
    })


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, id=pk, user=request.user)

    if request.method == 'POST':
        form = AdEditForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, "Your ad has been updated successfully.")
            return redirect('account')
    else:
        form = AdEditForm(instance=ad)

    context = {
        'form': form,
        'ad': ad
    }
    return render(request, 'ad_edit.html', context)


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, id=pk, user=request.user)

    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Your ad has been deleted successfully.')
        return redirect('account')

    context = {'ad': ad}
    return render(request, 'ad_confirm_delete.html', context)


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdCreateForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, "Your ad has been created successfully!")
            return redirect('account')
    else:
        form = AdCreateForm()

    context = {'form': form}
    return render(request, 'ad_create.html', context)


@login_required
def cancel_proposal(request, proposal_id):
    proposal = get_object_or_404(
        ExchangeProposal, 
        id=proposal_id, 
        ad_sender=request.user
    )
    if proposal.condition == 'pending':
        proposal.condition = 'canceled'
        proposal.save()
        messages.success(request, 'Proposal canceled.')
    return redirect('account')

@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(
        ExchangeProposal,
        id=proposal_id,
        ad_receiver__user=request.user
    )
    if proposal.condition == 'pending':
        proposal.condition = 'accepted'
        proposal.save()
        messages.success(request, 'Proposal accepted successfully!')
    return redirect('account')

@login_required
def decline_proposal(request, proposal_id):
    proposal = get_object_or_404(
        ExchangeProposal,
        id=proposal_id,
        ad_receiver__user=request.user
    )
    if proposal.condition == 'pending':
        proposal.condition = 'declined'
        proposal.save()
        messages.success(request, 'Proposal declined.')
    return redirect('account')

