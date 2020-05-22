import time
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings


@api_view(['GET'])
def generate_H12(request):

    res = settings.DEFAULT_RESPONSE_AS_DICT.copy()

    time.sleep(31)

    res["status"] = True
    res["message"] = "Success"
    return JsonResponse(res)


@api_view(['GET'])
def generate_500(request):

    res = settings.DEFAULT_RESPONSE_AS_DICT.copy()

    1 / 0

    res["status"] = True
    res["message"] = "Success"
    return JsonResponse(res)
