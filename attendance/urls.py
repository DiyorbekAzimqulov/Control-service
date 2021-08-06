from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import OrganizationView, EmployeeView, ComeIn, DaySummaryView, CreateUserView, CustomAuthToken


urlpatterns = [
    path('user', CreateUserView.as_view(), name='user'),
    path('auth-token', CustomAuthToken.as_view(), name='auth-token'),
    path('organization', OrganizationView.as_view(), name='organization'),
    path('employee', EmployeeView.as_view(), name='employee'),
    path('enrance', ComeIn.as_view(), name='entrance'),
    path('summary', DaySummaryView.as_view(), name='summary')
]
urlpatterns = format_suffix_patterns(urlpatterns)