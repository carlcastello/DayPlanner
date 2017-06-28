
from django.contrib.auth.views import login, logout
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/$', login, {'template_name':'login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name = 'logout' ),

    url(r'^$', views.HomeView.as_view(), name = 'home' ),
    url(r'^(?P<date>[0-9-]+)/$', views.HomeView.as_view(), name = 'home' ),

    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name = 'profile'),

    url(r'^registered-users/$', views.RegisteredUsersView.as_view(), name = 'registered_users' ),
    url(r'^registered-users/users/(?P<pk>[0-9]+)/$', views.DetailUserView.as_view(), name = 'user_detail_view'),
		
    url(r'^schedule-planner/$', views.SchedulePlannerView.as_view(), name = 'schedule_planner' ),
    url(r'^schedule-planner/(?P<date>[0-9-]+)/$', views.SchedulePlannerView.as_view(), name = 'schedule_planner' ),

    # url(r'^schedule-planner/export-schedule/$', views.SchedulePDFView.as_view(), name = 'schedule_pdf' ),
    url(r'^schedule-planner/(?P<date>[0-9-]+)/(?P<store>[0-9a-f- ]+)/$', views.SchedulePDFView.as_view(), name = 'schedule_pdf' ),
    # url(r'^schedule-planner/(?P<date>[0-9-]+)/export-schedule/$', views.SchedulePDFView.as_view(), name = 'schedule_pdf' ),

    url(r'^time-clock/$', views.TimeClockView.as_view(), name = 'time_clock' ),
]