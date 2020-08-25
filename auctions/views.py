from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import operator
from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm 

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
    current = Bid.objects.filter(listing=listing).first()
    comments = Comment.objects.filter(listing=listing).all().order_by('-pk')
    if not listing:
        return HttpResponseRedirect(reverse('index'))    
    if listing in Listing.objects.filter(watchers=request.user.id):
        inlist = True
    else:
        inlist = False

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'inlist': inlist,
        'form': BidForm(),
        'current': current,
        'comments': comments
    })




# Adds item to watchlist and redirects
def watch(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.add(listing)

        return HttpResponseRedirect(reverse('watchlist'))


# Removes item from watchlist
def unwatch(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        request.user.watchlist.remove(listing)

        return HttpResponseRedirect(reverse('watchlist'))





# Renders users watchlist
def watchlist(request):
    watched = Listing.objects.filter(watchers=request.user.id)
    return render(request, 'auctions/watchlist.html', {
        'watched': watched
    })

# Registers a bid and applies the appropriate changes to db
def bid(request, listing_id):
    if request.method == 'POST':
        form = BidForm(request.POST)
        bid = float(form['bid'].value())
        listing = Listing.objects.get(pk=listing_id)
        # Ensure bid is larger than current bid
        if listing.current_bid > bid:
            return render(request, 'auctions/error.html')

        listing.current_bid = bid
        listing.save()

        record = Bid(current_bidder=request.user, listing=listing)
        record.save()

        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


# Allows user who created listing to close it.
def close(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.closed = True
       
        listing.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


def comment(request, listing_id):
    if request.method == 'POST':
        content = request.POST['content']
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment(user=request.user, listing=listing, content=content)
        comment.save()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


def category(request, category):
    

    
    if category == 'all':
        listings = Listing.objects.all().order_by('-pk')
    if category == 'pets':
        listings = Listing.objects.filter(category='pet supplies').all()
    else:
        listings = Listing.objects.filter(category=category).all()

    title = category.capitalize()

    return render(request, 'auctions/category.html', {
        'listings': listings,
        'title': title
    })