from django.contrib import admin
from django.urls import path
from market.views import show_cars, audi_purchase, payment
from market.views_auth import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_cars),
    path('buy_car/<int:id_>', audi_purchase),
    path('payment/<int:id_>', payment),
    path('login', login),
    path('logout', logout),
]
