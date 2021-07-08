from django.shortcuts import render


def personal_home_view(request):
    context = {}
    context["some_string"] = "this is some string from view :) "

    return render(request, "studies/personal_home.html", context)
