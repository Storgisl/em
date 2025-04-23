from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('ads/<uuid:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/', views.ads_view, name='ads'),
    path('ads/<uuid:ad_id>/exchange/', views.send_exchange_proposal, name='send_exchange'),
    path('ads/<uuid:pk>/edit/', views.ad_edit, name='ad_edit'),
    path('ads/<uuid:ad_id>/exchange/', views.send_exchange_proposal, name='send_exchange'),
    path('ads/create/', views.ad_create, name='ad_create'),
    path('proposals/<uuid:proposal_id>/accept/', views.accept_proposal, name='proposal_accept'),
    path('proposals/<uuid:proposal_id>/decline/', views.decline_proposal, name='proposal_decline'),
    path('proposals/<uuid:proposal_id>/cancel/', views.cancel_proposal, name='proposal_cancel'),
]
