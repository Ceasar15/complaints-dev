from django.urls import path
from apps.Auth.views import MyObtainTokenPairView, RegisterView, ProfileViewPost, ProfileViewUpdate, ProfileViewGet, \
    EmergencyContactsView, logout_view, ComplaintsFormView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    # path('profile-post/', ProfileViewPost.as_view(), name='profile_post'),
    path('profile-get/', ProfileViewGet.as_view(), name='profile_post'),
    path('profile-update/<int:user_id>', ProfileViewUpdate.as_view(), name='profile_update'),
    path('emergency-contacts/', EmergencyContactsView.as_view(), name='emergency_contacts'),
    path('complaints-form/', ComplaintsFormView.as_view(), name='complaints-dev-form'),
    path('logout/', logout_view, name='logout'),

]
