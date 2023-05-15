from django.urls import path
from . import views

urlpatterns = [
    path('stocks_price_predictor/<str:symbol>/', views.stocks_price_predictor, name='stocks_price_predictor')

]
