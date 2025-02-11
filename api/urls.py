from django.urls import path
from . import views
from rest_framework_simplejwt.views import ( 
    TokenObtainPairView,
    TokenRefreshView,)

urlpatterns = [
    # Generate token on login to be stored in the browser. 
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # When the token expires, refresh and generate a new token that updates the old token. 
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
]