from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TBCarsWeb

# 🏠 Index
def index(request):
    return render(request, "carsapp/index.html")

# ➕ CREATE
def createcar(request):
    if request.method == "POST":
        carname = request.POST.get("carname")
        carbrand = request.POST.get("carbrand")
        carmodel = request.POST.get("carmodel")
        carprice = request.POST.get("carprice")

        if TBCarsWeb.objects.filter(carname=carname).exists():
            messages.warning(request, f"⚠️ Car '{carname}' already exists.")
        else:
            TBCarsWeb.objects.create(
                carname=carname, carbrand=carbrand,
                carmodel=carmodel, carprice=carprice
            )
            messages.success(request, f"✅ Car '{carname}' successfully added!")
        return redirect("readcar")
    return render(request, "carsapp/createcar.html")

# 📋 READ
def readcar(request):
    cars = TBCarsWeb.objects.all()
    return render(request, "carsapp/readcar.html", {"cars": cars})

# ✏️ UPDATE
def updatecar(request):
    if request.method == "POST":
        carname = request.POST.get("carname")
        carbrand = request.POST.get("carbrand")
        carmodel = request.POST.get("carmodel")
        carprice = request.POST.get("carprice")

        try:
            car = TBCarsWeb.objects.get(carname=carname)
            car.carbrand = carbrand or car.carbrand
            car.carmodel = carmodel or car.carmodel
            car.carprice = carprice or car.carprice
            car.save()
            messages.success(request, f"✅ Car '{carname}' updated successfully!")
        except TBCarsWeb.DoesNotExist:
            messages.error(request, f"❌ Car '{carname}' not found.")
        return redirect("readcar")
    return render(request, "carsapp/updatecar.html")

# 🗑️ DELETE
def deletecar(request):
    if request.method == "POST":
        carname = request.POST.get("carname")
        deleted, _ = TBCarsWeb.objects.filter(carname=carname).delete()
        if deleted:
            messages.success(request, f"🗑️ Car '{carname}' deleted successfully!")
        else:
            messages.warning(request, f"⚠️ Car '{carname}' not found.")
        return redirect("readcar")
    return render(request, "carsapp/deletecar.html")

# 🔍 SEARCH
def searchcar(request):
    car = None
    searched = False
    if request.method == "POST":
        searched = True
        carname = request.POST.get("carname")
        car = TBCarsWeb.objects.filter(carname__iexact=carname).first()
        if car:
            messages.success(request, f"✅ Found car '{carname}'!")
        else:
            messages.warning(request, f"❌ Car '{carname}' not found.")
    return render(request, "carsapp/searchcar.html", {"car": car, "searched": searched})
