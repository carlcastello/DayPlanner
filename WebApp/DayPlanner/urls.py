
from django.contrib.auth.views import login, logout
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/$', login, {'template_name':'login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name = 'logout' ),

    url(r'^$', views.HomeView.as_view(), name = 'home' ),
    url(r'^users/$', views.RegisteredUsersView.as_view(), name = 'registered_users' ),
	url(r'^users/delete-user/(?P<pk>\d+)/$', views.DeleteUserView.as_view(), name = 'delete_users' ),

	url(r'^users/create-store/(?P<store_name>[A-Za-z0-9 ]+)/(?P<store_address>[A-Za-z0-9 ]+)/$', views.CreateStoreView.as_view(), name = 'create_store' ),
	url(r'^users/delete-store/(?P<pk>[0-9a-f-]+)/$', views.DeleteStoreView.as_view(), name = 'delete_store' ),

    url(r'^planner/$', views.SchedulePlannerView.as_view(), name = 'schedule_planner' ),
    url(r'^planner/(?P<date>[0-9-]+)/$', views.SchedulePlannerView.as_view(), name = 'schedule_planner' ),
    url(r'^clock/$', views.TimeClockView.as_view(), name = 'time_clock' ),
]