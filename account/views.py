import logging

from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard


logger = logging.getLogger(__name__)


# @login_required
def AccountView(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your KYC.")
            return redirect("account:kyc-reg")

        account = Account.objects.get(user=request.user)
    else: 
        messages.warning(request, "You need to login to access the dashboard.")
        return redirect("user_auths:sign-in")
    
    context = {
        "kyc": kyc,
        "account": account,
    }
    return render(request, "account/account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    try: 
        kyc = KYC.objects.get(user=user)
    except: 
        kyc = None
        
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "Your KYC form has been successfully submitted and is currently pending review.")
            return redirect("core:index")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "account/kyc-form.html", context)

def dashboard(request):
    
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your KYC.")
            return redirect("account:kyc-reg")

        account = Account.objects.get(user=request.user)
        credit_cards = CreditCard.objects.filter(user=request.user).order_by("-id")
        
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                card_id = new_form.card_id
                messages.success(request, "Card has been added successfully.")
                return redirect("account:dashboard")
            else:
                messages.error(request, "There was an error adding your card. Please check the details and try again.")
        else: 
            form = CreditCardForm(request.POST)     
    else: 
        messages.warning(request, "You need to login to access the dashboard.")
        return redirect("user_auths:sign-in")

    context = {
        "CreditCardForm": form,
        "kyc": kyc,
        "account": account,
        "credit_cards": credit_cards
    }
    return render(request, "account/dashboard.html", context) 
