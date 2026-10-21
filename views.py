from django.shortcuts import render

from plugins.pdf_viewer import forms


def manager(request):
    form = forms.DummyManagerForm()

    template = 'pdf_viewer/manager.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
