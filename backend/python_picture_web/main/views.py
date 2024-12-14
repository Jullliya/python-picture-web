from django.http import JsonResponse
from django.shortcuts import HttpResponse
from .models import Analyse
from users.models import Users
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
import json
import requests

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

        image = request.FILES.get('image')
        if not image:
            return HttpResponse('Файл изображения обязателен.', status=400)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d.%m.%Y в %H:%M")
        model_1 = request.POST.get('model_1')
        model_2 = request.POST.get('model_2')
        model_3 = request.POST.get('model_3')
        ensemble = request.POST.get('ensemble')
        model_1_probability = request.POST.get('model_1_probability')
        model_2_probability = request.POST.get('model_2_probability')
        model_3_probability = request.POST.get('model_3_probability')
        ensemble_probability = request.POST.get('ensemble_probability')
        patient = request.POST.get('patient')
        description = request.POST.get('description')

        if not all([model_1, model_2, model_3, ensemble,model_1_probability, model_2_probability, model_3_probability, ensemble_probability, patient, description]):
            return HttpResponse('Отсутствуют обязательные параметры.', status=400)

        analyse = Analyse.objects.create(
            user_key=user,
            image=image,
            datetime=formatted_datetime,
            model_1=model_1,
            model_2=model_2,
            model_3=model_3,
            ensemble=ensemble,
            model_1_probability=model_1_probability,
            model_2_probability=model_2_probability,
            model_3_probability=model_3_probability,
            ensemble_probability=ensemble_probability,
            patient=patient,
            description=description
        )

        return JsonResponse({
            "success": True,
            "message": "Запись успешно создана.",
            "data": {
                "id": analyse.id,
                "user_key": user.key,
                "image": analyse.image.url,
                "date": analyse.datetime,
                "model_1": analyse.model_1,
                "model_2": analyse.model_2,
                "model_3": analyse.model_3,
                "model_1_probability": analyse.model_1_probability,
                "model_2_probability": analyse.model_2_probability,
                "model_3_probability": analyse.model_3_probability,
                "ensemble_probability": analyse.ensemble_probability,
                "result": analyse.ensemble,
                "patient": analyse.patient,
                "description": analyse.description,
                "diagnosis": analyse.diagnosis
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
                "image": record.image.url,
                "date": record.datetime,
                "model_1": record.model_1,
                "model_2": record.model_2,
                "model_3": record.model_3,
                "model_1_probability": record.model_1_probability,
                "model_2_probability": record.model_2_probability,
                "model_3_probability": record.model_3_probability,
                "ensemble_probability": record.ensemble_probability,
                "ensemble": record.ensemble,
                "patient": record.patient,
                "description": record.description,
                "diagnosis": record.diagnosis
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
        analyse = Analyse.objects.get(id=row_id, user_key=user)

        if os.path.exists('python_picture_web' + str(analyse.image.url)):
            os.remove('python_picture_web' + str(analyse.image.url))
            analyse.delete()
        else:
            return HttpResponse("Picture not found", status=404)

        if Analyse.objects.filter(id=row_id, user_key=user):
            return HttpResponse(False, status=200)
        else:
            return HttpResponse(True, status=200)

    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)

def delete_all(request, key):
    if request.method == "GET":
        try:
            user = Users.objects.get(key=key)
        except Users.DoesNotExist:
            return HttpResponse('Пользователь с таким ключом не найден.', status=404)

        analyses = Analyse.objects.filter(user_key=user)
        for analyse in analyses:
            if os.path.exists('python_picture_web' + str(analyse.image.url)):
                os.remove('python_picture_web' + str(analyse.image.url))
                analyse.delete()
            else:
                return HttpResponse("Picture not found", status=404)

        if Analyse.objects.filter(user_key=user):
            return HttpResponse(False, status=200)
        else:
            return HttpResponse(True, status=200)

    return JsonResponse({"success": False, "message": "Метод не поддерживается."}, status=405)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def classification_image(request: Request, key):
    method_name = "classification_image"
    try:
        image = request.FILES['image']
        image_data = image.read()
        result = MainImageClassifierBySkinLesion().apply(image_data)

        individual_labels = [label for label, _ in result['individual_predictions']]
        individual_probability = [max(probability) for _, probability in result['individual_predictions']]
        ensemble_label = result['ensemble_prediction'][0]

        model_1 = individual_labels[0]
        model_2 = individual_labels[1]
        model_3 = individual_labels[2]
        ensemble = ensemble_label

        model_1_probability =individual_probability[0]
        model_2_probability =individual_probability[1]
        model_3_probability =individual_probability[2]
        ensemble_probability = max(result['ensemble_prediction'][1])

        data = {
            "model_1": model_1,
            "model_2": model_2,
            "model_3": model_3,
            "ensemble": ensemble,
            "model_1_probability": model_1_probability,
            "model_2_probability": model_2_probability,
            "model_3_probability": model_3_probability,
            "ensemble_probability": ensemble_probability,
            "patient": request.POST.get('patient'),
            "description": request.POST.get('description')
        }

        files = {"image": (image.name, image_data, image.content_type)}
        response = requests.post(f'http://back:8000/cnn_table/{key}/add', data=data, files=files)
        return Response(response)
    except Exception as exc:
        response_status = status.HTTP_400_BAD_REQUEST
        exception = exc
        return Response({'error': str(exception)}, status=response_status)


@csrf_exempt
def update_analyse(request, key):
    if request.method == 'POST':
        try:
            user = Users.objects.get(key=key)
        except Users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Пользователь не найден.'}, status=404)

        try:
            data = json.loads(request.body.decode('utf-8'))
            record_id = data.get('id')
            description = data.get('description')
            diagnosis = data.get('diagnosis')

            if not all([record_id, description, diagnosis]):
                return JsonResponse({'success': False, 'message': 'Не все обязательные поля заполнены.'}, status=400)

            analyse = Analyse.objects.get(id=record_id, user_key=user)
            analyse.description = description
            analyse.diagnosis = diagnosis
            analyse.save()

            return JsonResponse({'success': True, 'message': 'Запись успешно обновлена.'})
        except Analyse.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Запись не найдена.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ошибка: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Метод не поддерживается.'}, status=405)
