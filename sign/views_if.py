""".,./
For event interface
"""

from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError


def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message':'event id already exists'})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message':'event name already exists'})

    if status == '':
        status = 1

    try:
        Event.objects.create(id=eid,
                             name=name,
                             status=int(status),
                             limit=limit,
                             address=address,
                             start_time=start_time)
    except ValidationError as e:
        error = 'start_time formate error, should be YYYY-MM-DD HH:MM:SS fromat.'
        return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': 'add event success'})


# def add_guest(request):
#     eid = request.POST.get('eid', '')
#     realname = request.POST.get('realname', '')
#     phone = request.POST.get('phone', '')
#     email = request.POST.get('email', '')
#     sign = request.POST.get('sign', '')

#     if eid == '' or realname == '' or phone == '':
#         return JsonResponse({'status': 10021, 'message': 'parameter error'})

#     result = Event.objects.filter(id=eid)
#     if result:
#         return JsonResponse({'status': 10022, 'message':'event id already exists'})

#     result = Event.objects.filter(name=name)
#     if result:
#         return JsonResponse({'status': 10023, 'message':'event name already exists'})

#     if status == '':
#         status = 1

#     try:
#         Event.objects.create(id=eid,
#                              name=name,
#                              status=int(status),
#                              limit=limit,
#                              address=address,
#                              start_time=start_time)
#     except ValidationError as e:
#         error = 'start_time formate error, should be YYYY-MM-DD HH:MM:SS fromat.'
#         return JsonResponse({'status': 10024, 'message': error})

#     return JsonResponse({'status': 200, 'message': 'add event success'})
