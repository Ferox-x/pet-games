from django.urls import path
from django.contrib.auth.decorators import login_required
from support.views import SupportView, SupportStaffView

app_name = 'support'

urlpatterns = [
    path('', login_required(SupportView.as_view()),
         name='support'
         ),
    path('staff/', login_required(SupportStaffView.as_view()),
         name='support_staff'
         ),
]
