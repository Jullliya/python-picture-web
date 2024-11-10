from django.shortcuts import HttpResponse
from .models import Analyse
from .forms import ImageForm


# Create your views here.
def cnn_result_post(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)


def get_result(request):
    if request.method == "GET":
        analyse = list(Analyse.objects.values())
        return HttpResponse(analyse)


def delete_row(request):
    if request.method == "GET":
        row_id = request.GET.get("id")
        Analyse.objects.filter(id=row_id).delete()
        if Analyse.objects.filter(id=row_id):
            return HttpResponse(False)
        else:
            return HttpResponse(True)
