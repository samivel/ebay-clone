from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import operator
from .models import User, Listing
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all().order_by('-pk')
    

    
    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



# Create new listing
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        # Get data from post request
        title = form['title'].value()
        description = form['description'].value()
        bid = form['starting_bid'].value()
        image = form['image_url'].value()
        if not image:
            image = "https://sisterhoodofstyle.com/wp-content/uploads/2018/02/no-image-1.jpg"
        category = form['category'].value()
        # create new Listin object and save
        listing = Listing(title=title, description=description,
                            current_bid=bid, image_url=image, category=category, seller=request.user.id)
        listing.save()
        return HttpResponseRedirect(reverse('index'))


    return render(request, 'auctions/create.html', {
        'form': ListingForm()
    })



def listing(request, listing_id):
    listing = Listing.objects.filter(pk=listing_id).first()
    if not listing:
        return HttpResponseRedirect(reverse('index'))    


    return render(request, 'auctions/listing.html', {
        'listing': listing
    })

