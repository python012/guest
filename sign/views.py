from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from sign.models import Event, Guest


# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error_message': 'username or password is not correct!'})

        # if username == 'admin' and password == 'admin123':
            # return HttpResponse('Login success!')
            # return HttpResponseRedirect('/event_manage/')
            # response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600) # add browser cookie
            # request.session['user'] = username
            # return response
        # else:
            # return render(request, 'index.html', {'error_message': 'username or password is not correct!'})


@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '') # read the cookie from browser
    username = request.session.get('user', '')  # read browser session
    event_list = Event.objects.all()
    # return render(request, "event_manage.html", {"user": username})
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()

    paginator = Paginator(guest_list, 3)
    page_number = request.GET.get('page')

    try:
        contacts = paginator.page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


@login_required
def search_guest(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    guest_list = Guest.objects.filter(realname__contains=search_name)

    paginator = Paginator(guest_list, 3)
    page_number = request.GET.get('page')

    try:
        contacts = paginator.page(page_number)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username, "guests": contacts})
