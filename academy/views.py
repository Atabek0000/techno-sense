from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request, Client, Master
from .forms import RequestForm, MasterSignUpForm, ClientSignUpForm
from django.contrib.auth import authenticate, login, logout


@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.client = Client.objects.get(user=request.user)
            request_obj.save()
            return redirect('client_page')
    else:
        form = RequestForm()
    return render(request, 'orders/create_request.html', {'form': form})


@login_required
def client_page(request):
    client = get_object_or_404(Client, user=request.user)
    requests = Request.objects.filter(client=client)
    return render(request, 'orders/client_page.html', {'requests': requests})


@login_required
def master_page(request):
    master = get_object_or_404(Master, user=request.user)
    requests = Request.objects.filter(master=master)
    return render(request, 'orders/master_page.html', {'requests': requests})


@login_required
def accept_request(request, request_id):
    request_obj = Request.objects.get(id=request_id)
    if request.user.master == request_obj.master:
        request_obj.status = 'Отклонить'
        request_obj.save()
    return redirect('master_page')


@login_required
def reject_request(request, request_id):
    request_obj = Request.objects.get(id=request_id)
    if request.user.master == request_obj.master:
        request_obj.status = 'Принять'
        request_obj.save()
    return redirect('master_page')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'client'):
                return redirect('client_page')
            elif hasattr(user, 'master'):
                return redirect('master_page')
        else:
            return render(request, 'orders/login.html', {'error': 'Invalid username or password'})
    return render(request, 'orders/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_master(request):
    if request.method == 'POST':
        form = MasterSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = MasterSignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def register_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ClientSignUpForm()
    return render(request, 'registration/register.html', {'form': form})
