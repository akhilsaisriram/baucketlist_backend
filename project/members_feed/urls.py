from django.urls import path
from .views import *


urlpatterns = [
    path('Add_bucket_feed', Add_bucket_feed.as_view()),
    path('FeedView', FeedView.as_view()),
    path('Delete_feed',Delete_feed.as_view()),
    path('Update_feed',Update_feed.as_view()),



]