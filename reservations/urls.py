from django.urls import path

from reservations.views import AdminReservationListView, CreateReservationView, MyReservationDeleteView, \
    MyReservationDetailView, \
    MyReservationListView

app_name = "reservations"


urlpatterns = [
    path("create/", CreateReservationView.as_view(), name="create_reservation"),
    path("my/", MyReservationListView.as_view(), name="my_reservations"),
    path("my/<int:pk>/", MyReservationDetailView.as_view(), name="my_reservation_detail"),
    path("my/<int:pk>/delete/", MyReservationDeleteView.as_view(), name="my_reservation_delete"),
    path("all/", AdminReservationListView.as_view(), name="all_reservations"),
]
