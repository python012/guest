import time

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sign.models import Event, Guest


@csrf_exempt
def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    attendees_limit = request.POST.get('attendees_limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    if eid == '' or name == '' or attendees_limit == '' or address == '' or start_time == '':
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
                             attendees_limit=attendees_limit,
                             address=address,
                             start_time=start_time)
    except ValidationError:
        error = 'start_time formate error, should be YYYY-MM-DD HH:MM:SS fromat.'
        return JsonResponse({'status': 10024, 'message': error})

    return JsonResponse({'status': 200, 'message': 'add event success'})


@csrf_exempt
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    # sign = request.POST.get('sign', '')

    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message':'event id is invalid'})

    result = Event.objects.filter(name=eid).status

    if not result:
        return JsonResponse({'status': 10023, 'message':'event status is not available'})

    event_limit = Event.objects.get(id=eid).attendees_limit
    guest_limit = len(Guest.objects.filter(event_id=eid))

    if guest_limit >= event_limit:
        return JsonResponse({'status': 10024, 'message':'event number is full'})

    event_time = Event.objects.get(id=eid).start_time

    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, r"%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'message':'event is out of date'})

    try:
        Guest.objects.create(event_id=eid,
                             realname=realname,
                             phone=int(phone),
                             email=email,
                             sign=False)
    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})

    return JsonResponse({'status': 200, 'message': 'add event success'})


@csrf_exempt
def get_event_list(request):
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
                    datas = []
                    r = Event.objects.get(id=eid)
                    event = {}
                    event['id'] = r.id
                    event['name'] = r.name
                    event['status'] = r.status
                    event['address'] = r.address
                    event['start_time'] = r.start_time
                    datas.append(event)
                    return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
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


@csrf_exempt
def get_guest_list(request):
    eid = request.GET.get('eid', '')
    phone = request.GET.get('phone', '')

    if eid == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status': 200, 'data': guest})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


@csrf_exempt
def user_sign(request):
    eid = request.POST.get('eid', '')
    phone = request.POST.get('phone', '')

    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, r"%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event is out of date'})

    result = Guest.objects.filter(phone=phone)

    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone null'})

    result = Guest.objects.filter(event_id=eid, phone=phone)

    if not result:
        return JsonResponse({'status': 10026, 'message': 'user did not participate in the event'})

    result = Guest.objects.get(event_id=eid, phone=phone).sign

    if result:
        return JsonResponse({'status': 10027, 'message': 'user has sign in already'})
    else:
        Guest.objects.get(event_id=eid, phone=phone).update(sign=True)
        return JsonResponse({'status': 200, 'message': 'sign success'})
