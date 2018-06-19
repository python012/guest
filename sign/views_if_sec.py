from django.contrib import auth as django_auth
from django.http import JsonResponse
import base64
from sign.models import Event


def _user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return 'null'
    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    if user is not None:
        django_auth.login(request, user)
        return 'success'
    else:
        return 'fail'


def get_event_list(request):
    auth_result = _user_auth(request)
    if auth_result == 'null':
        return JsonResponse({'status':10011, 'message':'user auth null'})
    
    if auth_result == 'fail':
        return JsonResponse({'status':10012, 'message':'user auth fail'})
    
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    if not eid:
        if not name:
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        results = Event.objects.filter(name__contains=name)

        if not len(results):
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            datas = []
            for r in results:
                event = {}
                event['id'] = r.id
                event['name'] = r.name
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
    else:
        result = Event.objects.get(id=eid)
        if not result:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            result = Event.objects.get(id=eid).status
            if not result:
                return JsonResponse({'status': 10023, 'message': 'event status is not available'})
            else:
                if not name:
                    r = Event.objects.get(id=eid)
                    event = {}
                    event['id'] = r.id
                    event['name'] = r.name
                    event['status'] = r.status
                    event['address'] = r.address
                    event['start_time'] = r.start_time
                    return JsonResponse({'status': 200, 'message': 'success', 'data': event})
                else:
                    results = Event.objects.filter(id=eid, name=name)
                    if not len(results):
                        return JsonResponse({'status': 10022, 'message': 'query result is empty'})
                    else:
                        datas = []
                        for r in results:
                            event = {}
                            event['id'] = r.id
                            event['name'] = r.name
                            event['status'] = r.status
                            event['address'] = r.address
                            event['start_time'] = r.start_time
                            datas.append(event)
                        return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
