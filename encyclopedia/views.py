from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    rawMarkdown = util.get_entry(title)
    if rawMarkdown is not None:
        html = markdown2.markdown(rawMarkdown)
        return render(request, "encyclopedia/layout.html", {
            "html": html,
            "title": title
        })
    else:
        return render(request, "encyclopedia/layout.html", {
            "title": title,
            "html": "<h1>Error! Page not found.</h1>"
        })


def search(request):
    # I referenced https://stackoverflow.com/questions/4706255/how-to-get-value-from-form-field-in-django-framework
    # to see how to grab the inputted value from the name field from the user submitted form.
    query = request.GET.get('q')
    entries = util.list_entries()
    res = []
    for entry in entries:
        if query.lower() == entry.lower():
            rawMarkdown = util.get_entry(query)
            html = markdown2.markdown(rawMarkdown)
            return render(request, "encyclopedia/layout.html", {
                "html": html,
                "title": query
            })
        if query.lower() in entry.lower():
            res.append(entry)
    if (len(res) == 0):
        return render(request, "encyclopedia/index.html", {
            "title": "Search Results",
            "html": "<h1> No matching search results. </h1>"
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": res,
            "searchBool": True
        })


def newpage(request):
    if request.method == "POST":
        entries = util.list_entries()
        newPageTitle = request.POST.get('newPageTitle')
        for entry in entries:
            if newPageTitle.lower() == entry.lower():
                return HttpResponse("ERROR! Page already exists")
        newPageContent = request.POST.get("newPageContent")
        util.save_entry(newPageTitle, newPageContent)
        html = markdown2.markdown(newPageContent)
        return render(request, "encyclopedia/layout.html", {
            "html": html,
            "title": newPageTitle
        })

    else:
        return render(request, "encyclopedia/newpage.html")


def editpage(request):
    title = request.GET.get('title')
    return HttpResponse(title)
