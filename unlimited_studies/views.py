from django.shortcuts import render


def home_screen_view(request):
    context = {}
    context["some_string"] = "Why learn ?? because ..."

    return render(request, "home.html", context)


def legal_view(request):
    return render(request, "term_use.html")
