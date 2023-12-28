from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_simplejwt.views import TokenRefreshView

from blog.views import RegisterView, MovieView, UserLogoutView, MovieDetailView, UserTokenObtainView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/login/', UserTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', MovieView.as_view()),
    path('movie-info/<pk>/', MovieDetailView.as_view()),
    path('movies/<pk>/', MovieView.as_view()),
    path('api/user/logout/', UserLogoutView.as_view(), name='auth_logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)