from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from security.decorators import editor_user_required, has_journal

from plugins.pdf_viewer import forms


@has_journal
@editor_user_required
def manager(request):
    form = forms.ManagerForm(journal=request.journal)

    if request.POST:
        form = forms.ManagerForm(request.POST, journal=request.journal)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Settings saved.')
            return redirect(reverse('pdf_viewer_manager'))

    template = 'pdf_viewer/manager.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
