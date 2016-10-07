from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html', context=None)


def results(request):
    return render(request, 'results.html', context=None)


def query1(request):
    if request.method == "POST":
        return True

    return False


def query2(request):
    if request.method == "POST":
        return True

    return False


def query3(request):
    if request.method == "POST":
        return True

    return False


def query4(request):
    if request.method == "POST":
        return True

    return False


def query5(request):
    if request.method == "POST":
        return True

    return False


def query6(request):
    if request.method == "POST":
        return True

    return False


def part3_1(request):
    if request.method == "POST":
        return True

    return False


def part3_2(request):
    if request.method == "POST":
        return True

    return False
