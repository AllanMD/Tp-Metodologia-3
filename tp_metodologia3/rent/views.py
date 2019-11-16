import random
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.db.models import Count

from rent.forms import CityForm
from rent.models import Property, City
from django.contrib.auth.models import User
from rent.models import Property, City, RentDate, Reservation
from tp_metodologia3.settings import ROOT_DIR


def login(request):
    
    form = AuthenticationForm()
    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                print('entro')
                return redirect('/')

    return render(request, "rent/login.html", {'form': form})

def signup(request):

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():

            user = form.save()

            if user is not None:
                do_login(request, user)
                return redirect('/')

    return render(request, "rent/signup.html", {'form': form})

def home(request, city_id=''):
    order_type = ''
    if city_id:
        city = City.objects.get(id=city_id)
    else:
        city = False

    if request.GET:
        order_type = request.GET['orderby']

    if order_type:
        if order_type == 'higher_price':
            propiedades_list = Property.objects.all().order_by('-price')
        elif order_type == 'lower_price':
            propiedades_list = Property.objects.all().order_by('price')
        elif order_type == 'higher_capacity':
            propiedades_list = Property.objects.all().order_by('-capacity')
        else:
            propiedades_list = Property.objects.all().order_by('capacity')
    else:
        propiedades_list = Property.objects.all()

    ciudades_list = City.objects.all()
    propiedades_por_ciudad = Property.objects.values('city').annotate(city_count=Count('city')).order_by(
        '-city_count')
    
    return render(request, "rent/home.html", {'propiedades_list': propiedades_list,
                                                            'ciudades_list': ciudades_list, 'root': ROOT_DIR,
                                                            'propiedades_por_ciudad': propiedades_por_ciudad,
                                                            'city': city})
    

def property(request, property_id):
    
        o = Property.objects.get(id=property_id)
        user = request.user
        dates = RentDate.objects.filter(property=o).filter(reservation=None)
        ciudades_list = City.objects.all()
        totalcapacity = o.capacity + 1
        capacity = range(1, totalcapacity)
        msg = ''

        if request.method == 'POST':
            date_list = request.POST.getlist('dates')
            my_reservation = Reservation(date=datetime.now(), reservationCode=random.randrange(999, 99999),
                                         total=int(o.price * len(date_list)), property=o, user=user)
            my_reservation.save()
            new_date_list = []
            for date in date_list:
                date_new = RentDate.objects.filter(date=date).first()
                date_new.reservation = my_reservation
                date_new.save()
                new_date_list.append(date_new)

            return render(request, "rent/reservationdetail.html",
                          {"reservation": my_reservation, "dates": new_date_list})

        return render(request, "rent/property.html",
                      {'ciudades_list': ciudades_list, 'property': o, 'capacity': capacity, 'dates': dates})
    


def reservation(request, reservation_id):
    if request.user.is_authenticated:
        my_reservation = Reservation.objects.filter(id=reservation_id).first()
        date_list = RentDate.objects.filter(reservation__id=reservation_id)

    return render(request, "rent/reservationdetail.html", {"reservation": my_reservation, "dates": date_list})


def propertyForm(request):

    ciudades_list = City.objects.all()
    error = ''
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['desc']
        capacity = request.POST['capacity']
        price = request.POST['price']
        city = request.POST['city']
        my_city = ciudades_list.filter(name=city).first()
        image = request.FILES.get('file')
        if name is not None:
            p = Property(name=name, description=description, price=price, capacity=capacity, city=my_city,
                           owner=request.user, image=image)
            p.save()
        else:
            error = 'Ups, algo ha ocurrido'
    if request.user.is_authenticated:
        return render(request, "rent/propertyform.html",
                      {'ciudades_list': ciudades_list, 'error': error, 'msg': msg})
    # else
    return redirect('/login')



def reservations(request):
    reservations = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            reservations = Reservation.objects.all()
        else:
            reservations = Reservation.objects.filter(user__id=request.user.id).all()

    return render(request, "rent/reservations.html", {"reservations": reservations})

    # En otro caso redireccionamos al login
    return redirect('/login')


def logout(request):
    do_logout(request)
    
    return redirect('/')
