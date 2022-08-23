from django.urls import path
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login_user,name="login"),
    path("logout/",authviews.LogoutView.as_view(),name="logout"),
    path("delete_user/",views.delete_user,name="delete-user"),
    path("change_password/",views.change_password,name="change-password"),
    path("privacy_settings/",views.privacy_settings,name="privacy-settings"),
    path("reset_password/",authviews.PasswordResetView.as_view(template_name="core/reset_pass.html"),name="reset-password"),
    path("reset_password_sent/",authviews.PasswordResetDoneView.as_view(template_name="core/reset_pass_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",authviews.PasswordResetConfirmView.as_view(template_name="core/reset_pass_confirm.html"),name="password_reset_confirm"),
    path("reset_password_complete/",authviews.PasswordResetCompleteView.as_view(template_name="core/reset_pass_complete.html"),name="password_reset_complete"),
    path("send_verify_email/<int:pk>/",views.send_verify_email,name="send-verify-email"),
    path("verify_email/<str:otp>/",views.verify_email,name="verify-email"),
    path("profile/<int:pk>/",views.profile,name="profile"),
    path("add_profile/",views.add_profile,name="add-profile"),
    path("edit_profile/",views.edit_profile,name="edit-profile"),
]