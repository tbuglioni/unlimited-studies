from django.conf import settings
from django.shortcuts import render, redirect


def personal_home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    context["some_string"] = "this is some string from view :) "

    return render(request, "studies/personal_home.html", context)
