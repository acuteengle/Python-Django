from django.shortcuts import render

from . import util
import markdown2 # https://github.com/trentm/python-markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    entry = util.get_entry(title) 

    if (entry):
        content = markdown2.markdown(entry)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page not found"
        })


def search(request):
    param = request.GET.get('q', '') # https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get

    entry = util.get_entry(param) 

    if (entry):
        content = markdown2.markdown(entry)
        return render(request, "encyclopedia/page.html", {
            "title": param,
            "content": content
        })
    else:
        results = []
        for entry in util.list_entries():
            if (param in entry):
                results.append(entry) 

        return render(request, "encyclopedia/results.html", {
            "results": results
        })


from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if (util.get_entry(title)):
                return render(request, "encyclopedia/error.html", {
                    "message": "An encyclopedia entry already exists with the provided title"
                })
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                entry = util.get_entry(title)
                content = markdown2.markdown(entry)
                return render(request, "encyclopedia/page.html", {
                    "title": title,
                    "content": content
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })


class EditEntryForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput()) # http://www.semicolom.com/blog/add-a-hidden-field-to-a-django-form/
    content = forms.CharField(label="Content", widget=forms.Textarea)


def edit(request):
    param = request.GET.get('q', '')

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            entry = util.get_entry(title)
            content = markdown2.markdown(entry)
            return render(request, "encyclopedia/page.html", {
                "title": title,
                "content": content
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": param,
                "form": form
            })
    else:
        entry = util.get_entry(param) 

        if (entry):
            return render(request, "encyclopedia/edit.html", {
                "title": param,
                "form": EditEntryForm(initial={'title': param, 'content': entry}) # https://stackoverflow.com/questions/7122071/how-can-i-fill-up-form-with-model-object-data
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Requested page not found"
            })


import random as rand

def random(request):
    entries = util.list_entries()
    index = rand.randrange(len(entries)) # https://docs.python.org/3/library/random.html

    title = entries[index]
    entry = util.get_entry(title) 
    content = markdown2.markdown(entry)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content
    })