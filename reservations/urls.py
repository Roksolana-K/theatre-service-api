from django.urls import path

from reservations.views import AdminReservationListView, CreateReservationView, MyReservationDeleteView, \
    MyReservationDetailView, \
    MyReservationListView

app_name = "cinema"


urlpatterns = [
    path("create-reservation/", CreateReservationView.as_view(), name="create_reservation"),
    path("my-reservations/", MyReservationListView.as_view(), name="my_reservations"),
    path("my-reservations/<int:pk>/", MyReservationDetailView.as_view(), name="my_reservation_detail"),
    path("my-reservations/<int:pk>/delete/", MyReservationDeleteView.as_view(), name="my_reservation_delete"),
    path("all-reservations/", AdminReservationListView.as_view(), name="all_reservations"),
]
