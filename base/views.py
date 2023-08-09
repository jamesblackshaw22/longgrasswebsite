from django.forms import ValidationError
from django.shortcuts import redirect, render
from .models import User, Field, Indecision, Status
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import IndecisionForm, JoinFieldForm, StatusForm, FieldForm

# Create your views here.
from django.http import HttpResponse


def index(request):
    global_code = Field.objects.get(id=1).code
    return redirect("home", global_code)


def loginPage(request):
    if request.user.is_authenticated:
        global_code = Field.objects.get(id=1).code
        return redirect("home", global_code)

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Username OR password does not exist")

    return render(request, "base/login.html")


def logoutUser(request):
    logout(request)
    return redirect("index")


def home(request, room_code):
    currrent_field = Field.objects.get(code=room_code)
    indecisions = Indecision.objects.filter(field=currrent_field)
    user_fields = Field.objects.filter(participants__id=request.user.id)
    num_fields = user_fields.count()

    context = {
        "indecisions": indecisions,
        "field": currrent_field,
        "fields": user_fields,
        "num_fields": num_fields,
    }
    return render(request, "base/home.html", context)


def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            global_field = Field.objects.get(id=1)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            global_field.participants.add(user)
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "An error occured during registration")

    context = {"form": form}
    return render(request, "base/register.html", context)


def createField(request):
    form = FieldForm()

    if request.method == "POST":
        newField = Field.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            creator=request.user,
        )
        newField.participants.add(request.user)
        return redirect("home", newField.code)

    context = {"form": form}
    return render(request, "base/field_form.html", context)


def createIndecision(request):
    if request.method == "POST":
        form = IndecisionForm(request.user, request.POST)

        if form.is_valid():
            indecision = form.save(commit=False)
            indecision.creator = request.user
            indecision.save()
        return redirect("home", indecision.field.code)
    else:
        form = IndecisionForm(request.user)

    context = {"form": form}
    return render(request, "base/indecision_form.html", context)


def joinField(request):
    form = JoinFieldForm(code=0)
    if request.method == "POST":
        form = JoinFieldForm(request.POST, code=request.POST.get("code"))
        if form.is_valid():
            cd = form.cleaned_data
            code = cd.get("code")
            field = Field.objects.get(code=code)
            field.participants.add(request.user)
            return redirect("home", field.code)

    context = {"form": form}
    return render(request, "base/join_field_form.html", context)
