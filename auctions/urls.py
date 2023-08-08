from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("categoryDisplay", views.categoryDisplay, name="categoryDisplay"),
    path("category/<int:category_id>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("addBid/<int:listing_id>", views.addBid, name="addBid"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
]
