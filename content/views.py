import requests
from django.shortcuts import render, redirect
from .models import Progress, News, City
from .forms import ProgressForm, NewsForm, CityForm


def main(request):
    return render(request, 'main.html')


def o_nas(request):
    return render(request, 'onas.html')


def progress_list(request):
    progresses = Progress.objects.all()
    return render(request, 'progress_list.html', {'progresses': progresses})


def progress_create(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('progress_list')
    else:
        form = ProgressForm()
    return render(request, 'progress_form.html', {'form': form})


def progress_update(request, pk):
    progress = Progress.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('progress_list')
    else:
        form = ProgressForm(instance=progress)
    return render(request, 'progress_form.html', {'form': form})


def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news_list.html', {'news': news})


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form})


def news_update(request, pk):
    news_item = News.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'news_form.html', {'form': form})


def weather_news(request):
    appid = 'b35c9ddb4c9dc5f59171ccf2e9188293'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.save(commit=False)
            res = requests.get(url.format(new_city.name)).json()
            if res.get("cod") == 200:
                new_city.temp = res["main"]["temp"]
                new_city.icon = res["weather"][0]["icon"]
                new_city.save()
            else:
                # Обработка ошибок API
                print(f"Error: API response error for city {new_city.name} - {res.get('message')}")
    else:
        form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res.get("cod") == 200:
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"],
                'humidity': res["main"]["humidity"],
                'visibility': res["wind"]["speed"]
            }
            all_cities.append(city_info)
        else:
            print(f"Error: API response error for city {city.name} - {res.get('message')}")

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather_news.html', context)


def Documentation(request):
    return render(request, 'Documentation.html')




