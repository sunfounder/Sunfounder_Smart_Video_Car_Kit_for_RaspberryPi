"""html_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^motor/forward', views.motor_forward),
    url(r'^motor/backward', views.motor_backward),
    url(r'^motor/stop', views.motor_stop),
    url(r'^camera/increase/y', views.camera_increase_y),
    url(r'^camera/decrease/y', views.camera_decrease_y),
    url(r'^camera/increase/x', views.camera_increase_x),
    url(r'^camera/decrease/x', views.camera_decrease_x),
    url(r'^camera/home', views.camera_home),
    url(r'^motor/set/speed/(\d{1,3})', views.motor_set_speed),
    url(r'^turning/(\d{1,3})', views.turning),
    url(r'^calibrate/getconfig', views.calibrate_get_config),
    url(r'^runmode', views.run_mode),
    url(r'^calibrationmode', views.calibration_mode),
    url(r'^calibrate/turning/(.)/(\d{1,3})', views.calibrate_turning),
    url(r'^calibrate/motor/run', views.calibrate_motor_run),
    url(r'^calibrate/motor/stop', views.calibrate_motor_stop),
    url(r'^calibrate/motor/left/reverse', views.calibrate_motor_left_reverse),
    url(r'^calibrate/motor/right/reverse', views.calibrate_motor_right_reverse),
    url(r'^calibrate/confirm', views.calibrate_confirm),
    url(r'^calibrate/pan/(.)/(\d{1,3})', views.calibrate_pan),
    url(r'^calibrate/tile/(.)/(\d{1,3})', views.calibrate_tile),
    url(r'^test/(.)/(\d{0,3})', views.test),
    url(r'^client/', views.client),
]
