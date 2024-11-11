from django.http import JsonResponse
from django.shortcuts import HttpResponse
from .models import Analyse
from users.models import Users
from django.views.decorators.csrf import csrf_exempt
import io

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from image_classifier.main.run import MainImageClassifierBySkinLesion
# Create your views here.
@csrf_exempt
def cnn_result_post(request, key):
    if request.method == 'POST':
        try:
            user = Users.objects.get(key=key)
        except Users.DoesNotExist:
            return HttpResponse('Пользователь с таким ключом не найден.', status=404)

        image = request.GET.get('image')
        model_1 = request.GET.get('model_1')
        model_2 = request.GET.get('model_2')
        model_3 = request.GET.get('model_3')
        ensemble = request.GET.get('ensemble')

        if not all([user, image, model_1, model_2, model_3, ensemble]):
            return HttpResponse('Отсутствуют обязательные параметры.', status=400)

        analyse = Analyse.objects.create(
            user_key=user,
            image=image,
            model_1=model_1,
            model_2=model_2,
            model_3=model_3,
            ensemble=ensemble
        )

        return JsonResponse({
            "success": True,
            "message": "Запись успешно создана.",
            "data": {
                "id": analyse.id,
                "user_key": user.key,
                "image": analyse.image,
                "model_1": analyse.model_1,
                "model_2": analyse.model_2,
                "model_3": analyse.model_3,
                "ensemble": analyse.ensemble
            }
        })

    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)


def get_result(request, key):
    if request.method == "GET":
        try:
            user = Users.objects.get(key=key)
        except Users.DoesNotExist:
            return HttpResponse('Пользователь с таким ключом не найден.', status=404)

        analyse_records = Analyse.objects.filter(user_key=user)

        if not analyse_records:
             return HttpResponse('Нет записей для данного пользователя.', status=404)

        analyse_data = [
            {
                "id": record.id,
                "image": record.image,
                "model_1": record.model_1,
                "model_2": record.model_2,
                "model_3": record.model_3,
                "ensemble": record.ensemble
            }
            for record in analyse_records
        ]

        return JsonResponse({'results': analyse_data}, safe=False)

    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)


def delete_row(request, key):
    if request.method == "GET":
        try:
            user = Users.objects.get(key=key)
        except Users.DoesNotExist:
            return HttpResponse('Пользователь с таким ключом не найден.', status=404)

        row_id = request.GET.get("id")
        Analyse.objects.filter(id=row_id, user_key=user).delete()
        if Analyse.objects.filter(id=row_id, user_key=user):
            return HttpResponse(False, status=200)
        else:
            return HttpResponse(True, status=200)

    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def classification_image(request: Request):
    method_name = "classification_image"
    try:
        image = request.FILES['image']
        image_data = image.read()
        result = MainImageClassifierBySkinLesion().apply(image_data)
        return Response(result)
    except Exception as exc:
        response_status = status.HTTP_400_BAD_REQUEST
        exception = exc
        return Response({'error': str(exception)}, status=response_status)
