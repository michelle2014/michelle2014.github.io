from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_departments", views.departments, name="departments"),
    re_path(r"^category/(?P<category>[^/]+)$", views.category, name="category"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("create", views.create, name="create"),
    re_path(r"^(?P<title>[^/]+)$", views.listing_view, name="listing_view"),
    re_path(
        r"^my_listing/(?P<title>[^/]+)$", views.my_listing_view, name="my_listing_view"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
