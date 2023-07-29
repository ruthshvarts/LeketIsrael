from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main, name='main'),
    path('LeketIsraelApp/', views.LeketIsraelApp, name='LeketIsraelApp'),
    path('results/', views.results, name='results'),
    path('registration/signup/', views.signup, name="signup"),
    path('HomePage/', views.HomePage, name='HomePage'),
    path('image/<str:leket_location>/<str:type>/<str:chag>/<slug:end_date>/<str:location_pred>/', views.show_image, name='show_image'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)