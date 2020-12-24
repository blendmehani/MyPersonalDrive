from django.shortcuts import render, redirect
from .forms import ContactUsForm


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        return redirect('main', request.user.username)
    else:
        context = {}
        if request.POST:
            form = ContactUsForm(request.POST)
            if form.is_valid():
                form.save()
                context['success_message'] = 'You contacted us successfully, ' \
                                             'we will contact you via the email address you provided.'
            else:
                context['contact_us_form'] = form
        else:
            form = ContactUsForm()
            context['contact_us_form'] = form
        return render(request, 'dashboard/landing_page.html', context)

