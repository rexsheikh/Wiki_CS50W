from django.shortcuts import render
from django.http import HttpResponse
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


def search(request, search):
    entries = util.list_entries()
    res = []
    for entry in entries:
        if search == entry:
            rawMarkdown = util.get_entry(search)
            html = markdown2.markdown(rawMarkdown)
            return render(request, "encyclopedia/layout.html", {
                "html": html,
                "title": search
            })
        if search in entry:
            res.append(entry)
    if (len(res) == 0):
        return render(request, "encyclopedia/layout.html", {
            "title": "Search Results",
            "html": "<h1> No matching search results. </h1>"
        })
    else:
        return (request, "encyclopedia/index.html", {
            "entries": res,
            "searchBool": True
        })
