from django.shortcuts import render, redirect
import markdown
from . import util
from django import forms

class NewEntry(forms.Form):
    entry_request = forms.CharField()

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
            if search.lower() in entry.lower():
                found_entry=True
                return redirect("page", title=search)
    if not found_entry:
        return render(request, "encyclopedia/nopage.html",{
            "title": search.capitalize()
            })
