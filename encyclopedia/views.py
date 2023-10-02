from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util

# index returns an unordered list of links to all of the wiki pages


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry returns the html of the given page (provided with the title parameter)
# If a title is not found, the user is presented with an error


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

# search uses the request provided by the user to look for matching strings
# or substrings. If there is an exact match, the user is taken to the page.
# A matching substring returns a list of possible entries.


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

# newpage presents a user with a blank textarea to input markdown to create a new page
# The user first inputs a title, and if it exists, they are presented with an error. Otherwise,
# The page is saved locally and presents in the index and searches.


def newpage(request):
    if request.method == "POST":
        entries = util.list_entries()
        newPageTitle = request.POST.get('newPageTitle')
        for entry in entries:
            if newPageTitle.lower() == entry.lower():
                return render(request, "encyclopedia/layout.html", {
                    "html": "<h1>ERROR! Page already exists</h1>",
                    "title": None})
        newPageContent = request.POST.get("newPageContent")
        util.save_entry(newPageTitle, newPageContent)
        html = markdown2.markdown(newPageContent)
        return render(request, "encyclopedia/layout.html", {
            "html": html,
            "title": newPageTitle
        })

    else:
        return render(request, "encyclopedia/newpage.html")

# editpage presents the user with a pages existing markdown in a textarea that can
# be edited. If the request method is get, they are presented with the existing markdown
# If the request method is post, the new markdown is saved, overwriting the old file.


def editpage(request):

    if request.method == "POST":
        title = request.POST.get('title')
        rawMarkdown = request.POST.get('updatedPage')
        util.save_entry(title, rawMarkdown)
        html = markdown2.markdown(rawMarkdown)
        return render(request, "encyclopedia/layout.html", {
            "html": html,
            "title": title
        })
    else:
        title = request.GET.get('title')
        rawMarkdown = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "editPage": True,
            "title": title,
            "rawMarkdown": rawMarkdown,
        })

# I referenced https://www.w3schools.com/python/ref_random_choice.asp for the randchoice function.
# I referenced https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/ for the redirect function

# randompage uses the random module to pick a random entry and renders the layout
# for that page.


def randompage(request):
    entries = util.list_entries()
    randTitle = random.choice(entries)
    html = markdown2.markdown(util.get_entry(randTitle))
    return render(request, "encyclopedia/layout.html", {
        "html": html,
        "title": randTitle
    })
