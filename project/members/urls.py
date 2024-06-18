from django.urls import path
from .views import *


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('gmaillogin', LoginViewgmail.as_view()),
    path('user', UserView.as_view()),
    path('deleter_user',Delete_user.as_view()),
    path('Update',Update_password.as_view()),
    path('update_list',Update_date_in_bucketlist.as_view()),
    path('Add_bucket',Add_bucket.as_view()),
    path("DeleteBucketElement",DeleteBucketElement.as_view()),
    path("Add_curlocation",Add_curlocation.as_view())


]