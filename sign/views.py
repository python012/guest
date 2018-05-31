from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


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
            response = HttpResponseRedirect('/event_manager/')
            return response
        else:
            return render(request, 'index.html', {'error_message': 'username or password is not correct!'})

        # if username == 'admin' and password == 'admin123':
            # return HttpResponse('Login success!')
            # return HttpResponseRedirect('/event_manager/')
            # response = HttpResponseRedirect('/event_manager/')
            # response.set_cookie('user', username, 3600) # add browser cookie
            # request.session['user'] = username
            # return response
        # else:
            # return render(request, 'index.html', {'error_message': 'username or password is not correct!'})


@login_required
def event_manager(request):
    # username = request.COOKIES.get('user', '') # read the cookie from browser
    username = request.session.get('user', '')  # read browser session
    return render(request, "event_manager.html", {"user": username})
