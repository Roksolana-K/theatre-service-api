from django.urls import path

from user.views import CreateUserView, DeleteUserView, ManageUserView, UserListView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("my-info/", ManageUserView.as_view(), name="my_info"),
    path("my-info/delete/", DeleteUserView.as_view(), name="my_info_delete"),
    path("all-users/", UserListView.as_view(), name="all_users"),
]
