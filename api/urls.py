from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.serializers import MyTokenObtainPairSerializer
from api.views import MyTokenObtainPairView, RegisterView,getProfile,updateProfile,FileUploadAPIView,QueryHandlerView,QueryResponseView
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()


urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/', getProfile, name='profile'),
    path('profile/update/', updateProfile, name='update-profile'),
    path('upload/', FileUploadAPIView.as_view(), name='file-upload'),
    path('query/', QueryHandlerView.as_view(), name='query_handler'),
    path('response/', QueryResponseView.as_view(), name='response'),

]
