from django.urls import path
from a_users.views import *

urlpatterns = [
    path('', profile_view, name="profile"),
    path('edit/', profile_edit_view, name="profile-edit"),
    path('onboarding/', profile_edit_view, name="profile-onboarding"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('emailchange/', profile_emailchange, name="profile-emailchange"),
    path('usernamechange/', profile_usernamechange, name="profile-usernamechange"),
    path('emailverify/', profile_emailverify, name="profile-emailverify"),
    path('delete/', profile_delete_view, name="profile-delete"),
    path('send-coins/<username>', transfer_coins, name="transfer-coins"),
    path('redeem/<username>', redeem_coins, name="redeem-coins"),
    path('users/', user_list_view, name="user-list"),

]
