import base64
import hashlib
import time

from django.contrib import auth as django_auth
from django.http import JsonResponse

from sign.models import Event
from sign.views_if import add_event as add_event_in_views_if
from sign.views_if import get_event_list as get_event_list_in_views_if


def _user_sign(request):
    '''user signature and timestamp'''
    if request.method == 'POST':
        client_time = request.POST.get('time', '')
        client_sign = request.POST.get('sign', '')
    else:
        return 'error'
    
    if client_time == '' or client_sign == '':
        return 'sign null'
    
    # server time
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    
    # check the time diff
    time_diff = int(server_time) - int(client_time)
    if time_diff >= 60:
        return 'timeout'
    
    # check signature
    api_key = '2018FIFAWorldCup'
    md5 = hashlib.md5()
    sign_str = client_time + api_key
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()

    if server_sign != client_sign:
        return 'sign fail'
    else:
        return 'sign success'


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


def add_event(request):
    sign_result = _user_sign(request)
    if sign_result == 'error':
        return JsonResponse({'status':10011, 'message':'request error'})
    elif sign_result == 'sign null':
        return JsonResponse({'status':10012, 'message':'user sign null'})
    elif sign_result == 'timeout':
        return JsonResponse({'status':10013, 'message':'user sign timeout'})
    elif sign_result == 'sign fail':
        return JsonResponse({'status':10014, 'message':'user sign error'})
    return add_event_in_views_if(request)


def get_event_list(request):
    auth_result = _user_auth(request)
    if auth_result == 'null':
        return JsonResponse({'status':10011, 'message':'user auth null'})
    
    if auth_result == 'fail':
        return JsonResponse({'status':10012, 'message':'user auth fail'})
    return get_event_list_in_views_if(request)
