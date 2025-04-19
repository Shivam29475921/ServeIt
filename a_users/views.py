from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import *
from .models import CoinTransaction


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'a_users/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'a_users/profile_edit.html', {'form': form, 'onboarding': onboarding})


@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')


@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():

            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')

            form.save()

            # Then Signal updates emailaddress and set verified to False

            # Then send confirmation email
            send_email_confirmation(request, request.user)

            return redirect('profile-settings')
        else:
            messages.warning(request, 'Email not valid or already in use')
            return redirect('profile-settings')

    return redirect('profile-settings')


@login_required
def profile_usernamechange(request):
    if request.htmx:
        form = UsernameForm(instance=request.user)
        return render(request, 'partials/username_form.html', {'form': form})

    if request.method == 'POST':
        form = UsernameForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Username updated successfully.')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Username not valid or already in use')
            return redirect('profile-settings')

    return redirect('profile-settings')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

    return render(request, 'a_users/profile_delete.html')


@login_required
def transfer_coins(request, username):
    recipient = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = CoinTransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            sender_profile = request.user.profile
            recipient_profile = recipient.profile

            if sender_profile.coin_balance >= amount and request.user != recipient:
                sender_profile.coin_balance -= amount
                recipient_profile.coin_balance += amount
                sender_profile.save()
                recipient_profile.save()

                CoinTransaction.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    amount=amount
                )
                messages.success(request, f"You sent {amount} coins to {recipient.username}")
            else:
                messages.error(request, "Transfer failed (insufficient coins or invalid recipient)")
            return redirect('profile', username=recipient.username)
    else:
        form = CoinTransferForm()

    return render(request, 'a_users/transfer.html', {'form': form, 'recipient': recipient})


def redeem_coins(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    coin_balance = profile.coin_balance
    context = {'coin_balance': coin_balance}
    return render(request, 'a_users/redeem_coins.html', context)


@login_required
def user_list_view(request):
    query = request.GET.get("q")
    users = User.objects.all()
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'a_users/user_list.html', {'users': users})
