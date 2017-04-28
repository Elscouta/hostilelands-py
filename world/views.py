from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


from game.models import VillageForm

##
# Homepage
#
def index(request):
    return render(request, 'world/index.html', {})

##
# Creates a new village
#
def newvillage(request):
    if (request.method == 'POST'):
    
        form = VillageForm(request.POST)

        if (form.is_valid()):
            village = form.save()

            return HttpResponseRedirect(village.get_absolute_url())
            
    else:
        form = VillageForm()

    return render(request, 'world/newvillage.html', { 'form' : form })
