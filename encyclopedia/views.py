import random

from django.db.models.functions import Random
from django.shortcuts import render, redirect
import markdown
from . import util
from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .util import list_entries


class NewEntry(forms.Form):
    title = forms.CharField(label="New title")
    content = forms.CharField(widget=forms.Textarea, label="New content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    desired_page = util.get_entry(title)
    if desired_page is None:
        return render(request, "encyclopedia/nopage.html", {
            "title": title.capitalize()
        })
    else:
        html_desired_page = markdown.markdown(desired_page) #converts the markdown file to readable html
        return render(request, "encyclopedia/page.html", {
            "title": title.capitalize(),
            "content": html_desired_page
        })

def search_entry(request):
    search = request.GET['q']
    found_entry = False
    for entry in util.list_entries():
            if search.lower() == entry.lower():
                found_entry=True
                return redirect("page", title=search)
    if not found_entry:
        return render(request, "encyclopedia/search_results.html",{
            "search": search.lower(),
            "entries": util.list_entries()
            })

def create_entry(request):
    if request.method == "POST":
        new_form = NewEntry(request.POST)
        if new_form.is_valid():
            new_title= new_form.cleaned_data["title"]
            new_content = new_form.cleaned_data["content"]
            found_entry = False
            for entry in util.list_entries():
                if new_title.lower() in entry.lower():
                    found_entry = True
                    new_form.add_error('title', 'Error: This entry already exists.')
                    return render(request, "encyclopedia/create.html", {
                        "form": new_form,
                        "new_title": new_title
                    })
            if not found_entry:
                filename = f"entries/{new_title.capitalize()}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
                default_storage.save(filename, ContentFile(new_content))
                return redirect("page", title=new_title)
    else:
        new_form = NewEntry()
        return render(request, "encyclopedia/create.html", {
                "form": new_form
        })


def edit_entry(request,title):

    if request.method == "POST":
        edited_entry = NewEntry(request.POST)
        if edited_entry.is_valid():
            new_title = edited_entry.cleaned_data["title"]
            new_content = edited_entry.cleaned_data["content"]
            util.save_entry(new_title, new_content)
            return redirect("page", title=new_title)

    else:
        edit_request= util.get_entry(title)
        if edit_request is None:
            return render(request, "encyclopedia/nopage.html", {
                "title": title.capitalize()
             })
        else:
            form_to_edit = NewEntry(initial={
                "title": title.capitalize(),
                "content": edit_request
            })
            return render(request, "encyclopedia/edit_entry.html", {
                "form": form_to_edit,
                "title": title.capitalize()
            })

def random_entry(request):
    random_number = random.randrange(len(list_entries()))
    return redirect("page",title=list_entries()[random_number])
