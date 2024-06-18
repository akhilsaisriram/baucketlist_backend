from django.urls import path
from .views import *


urlpatterns = [
    path('peoples_on_samedate', peoples_on_samedate.as_view()),
    path('send_message', Send_message.as_view()),
    path('get_message', Get_message.as_view()),
    # path('user', UserView.as_view()),
    # path('deleter_user',Delete_user.as_view()),
    # path('Update',Update_password.as_view()),
    # path('update_list',Update_date_in_bucketlist.as_view()),
    # path('Add_bucket',Add_bucket.as_view()),
    # path("DeleteBucketElement",DeleteBucketElement.as_view()),
    # path("Add_curlocation",Add_curlocation.as_view())


]