import json

from django.shortcuts import render, redirect

from .lib.queries import *


# Create your views here.


def index(request):
    return render(request, 'index.html', {'query': 0})


def results(request):
    return render(request, 'results.html', context=None)


def query1(request):
    if request.method == "POST":
        data = {
            'column_name': request.POST.get('column_name', ''),
            'column_value': request.POST.get('column_value', '')
        }

        count = two_1(data['column_name'], data['column_value'])

        return render(request, 'index.html', {
            'column_name': data['column_name'],
            'column_value': data['column_value'],
            'query': 1,
            'q_result': 1,
            'count': count
        })

    return redirect('index')


def query2(request):
    if request.method == "POST":
        data = {
            'column_name': request.POST.get('column_name', ''),
            'column_value': request.POST.get('column_value', ''),
        }

        drug = two_2(data['column_name'], data['column_value'])

        return render(request, 'index.html', {
            'column_name': data['column_name'],
            'column_value': data['column_value'],
            'query': 2,
            'q_result': 2,
            'drug': drug
        })

    return redirect('index')


def query3(request):
    if request.method == "POST":
        data = {
            'ds_name': request.POST.get('ds_name', ''),
            'mu_id': request.POST.get('mu_id', ''),
            'cl_id': request.POST.get('cl_id', ''),
        }

        exp = two_3(data['ds_name'], data['mu_id'], data['cl_id'])

        return render(request, 'index.html', {
            'ds_name': request.POST.get('ds_name', ''),
            'mu_id': request.POST.get('mu_id', ''),
            'cl_id': request.POST.get('cl_id', ''),
            'query': 3,
            'q_result': 3,
            'exp': exp
        })

    return redirect('index')


def query4(request):
    if request.method == "POST":
        data = {
            'ds_name': request.POST.get('ds_name', ''),
            'go_id': request.POST.get('go_id', ''),
        }

        t_test = two_4(data['go_id'],data['ds_name'])
        t_stat = t_test[0]
        p_value = t_test[1]

        return render(request, 'index.html', {
            'ds_name': request.POST.get('ds_name', ''),
            'go_id': request.POST.get('go_id', ''),
            'q_result': 4,
            'query': 4,
            'p_value': p_value,
            't_stat': t_stat,
        })

    return redirect('index')


def query5(request):
    if request.method == "POST":
        data = {
            'go_id': request.POST.get('go_id', ''),
            'disease_1': request.POST.get('disease_1', ''),
            'disease_2': request.POST.get('disease_2', ''),
            'disease_3': request.POST.get('disease_3', ''),
            'disease_4': request.POST.get('disease_4', ''),
        }

        diseases = [data['disease_1'], data['disease_2'], data['disease_3'], data['disease_4']]

        f_test = two_5(data['go_id'], diseases)
        f_stat = f_test[0]
        p_value = f_test[1]

        return render(request, 'index.html', {
            'go_id': request.POST.get('go_id', ''),
            'disease_1': request.POST.get('disease_1', ''),
            'disease_2': request.POST.get('disease_2', ''),
            'disease_3': request.POST.get('disease_3', ''),
            'disease_4': request.POST.get('disease_4', ''),
            'q_result': 5,
            'query': 5,
            'p_value': p_value,
            'f_stat': f_stat,
        })

    return redirect('index')


def query6(request):
    if request.method == "POST":
        data = {
            'go_id': request.POST.get('go_id', ''),
            'disease_1': request.POST.get('disease_1', ''),
            'disease_2': request.POST.get('disease_2', ''),
        }

        avg_correlations = two_6(data['go_id'], data['disease_1'], data['disease_2'])

        a_a = avg_correlations[0]
        a_b = avg_correlations[1]
        return render(request, 'index.html', {
            'go_id': request.POST.get('go_id', ''),
            'disease_1': request.POST.get('disease_1', ''),
            'disease_2': request.POST.get('disease_2', ''),
            'query': 6,
            'q_result': 6,
            'a_a': a_a,
            'a_b': a_b
        })

    return redirect('index')


def part3_1(request):
    if request.method == "POST":
        data = {
            'ds_name': request.POST.get('ds_name', ''),
        }

        if_gene = three_1(data['ds_name'])

        return render(request, 'index.html', {
            'ds_name': request.POST.get('ds_name', ''),
            'query': 7,
            'q_result': 7,
            'if_gene': if_gene,
        })

    return redirect('index')


def part3_2(request):
    if request.method == "POST":
        data = {
            'ds_name': request.POST.get('ds_name', ''),
        }

        result = three_2(data['ds_name'])

        positive = result[0]
        negative = result[1]

        return render(request, 'index.html', {
            'ds_name': request.POST.get('ds_name', ''),
            'query': 8,
            'q_result': 8,
            'positive': positive,
            'negative': negative,
        })

    return redirect('index')
