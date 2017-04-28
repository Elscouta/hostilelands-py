from django.db import transaction
from django.http import HttpResponse,JsonResponse

from game.exceptions import *

def json_handler(func):
    def decorated(request, *args, **kwargs):
        try:
            with transaction.atomic():

                ret = func(request, *args, **kwargs)
                ret["debug"] = { "path" : request.path }
                return JsonResponse(ret, status=200)

        except GameRulesViolation as e:
            return JsonResponse( { "error" : str(e) }, status=400)

        except ForbiddenError as e:
            return JsonResponse( { "error" : str(e) }, status=403)

        except InvalidIdentifier as e:
            return JsonResponse( { "error" : str(e) }, status=404)

        except InternalServerError as e:
            return JsonResponse( { "error" : "Internal Server Error" }, status=500)

    return decorated

def http_handler(func):
    def decorated(*args, **kwargs):
        try:
            with transaction.atomic():

                ret = func(*args, **kwargs)
                return HttpResponse(ret, status=200)

        except GameRulesViolation as e:
            return HttpResponse(str(e), status=400)

        except ForbiddenError as e:
            return HttpResponse(str(e), status=403)

        except InvalidIdentifier as e:
            return HttpResponse(str(e), status=404)

        except InternalServerError as e:
            return HttpResponse("Internal Server Error", status=500)

    return decorated
