from django.shortcuts import render
from django.http import Http404,  HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from django import forms

from . import util

import random as Random

markdowner = Markdown()


# Form to add an entry
class AddEntry(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"cols": 100}))


# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def entry(request, entry):
    allEntries = util.get_entry(entry)
    if allEntries == None:
        return render(request, "encyclopedia/error.html", {
            "title": 'Error',
            "message": 'No Entry found...'
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name": entry,
            "entry": markdowner.convert(allEntries)
        })


def random(request):
    entryList = util.list_entries()
    name = Random.choice(entryList)
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": name}))


def search(request):
    entry = request.POST["entry"]
    entryList = util.list_entries()
    if entry in entryList:
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": entry}))
    else:
        matchingEntry = []
        for entryName in entryList:
            if entry.lower() in entryName.lower():
                matchingEntry.append(entryName)
        return render(request, "encyclopedia/search.html", {
            "entries": matchingEntry,
            "count": len(matchingEntry)
        })


def add(request):
    if request.method == "POST":
        form = AddEntry(request.POST)
        if form.is_valid():
            title = form.data["title"]
            content = form.data["content"]
            allEntries = util.list_entries()
            for entry in allEntries:
                if title.lower() in entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "title": 'Error',
                        "message": 'Entry Already Exist'
                    })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        return render(request, "encyclopedia/add.html", {
            "form": AddEntry()
        })


def edit(request, entry):
    if request.method == "POST":
        title = entry
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        title = entry
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
            "entry": title,
            "content": content
        })