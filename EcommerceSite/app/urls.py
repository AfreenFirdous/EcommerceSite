from django.contrib import auth
from django.urls import path
from django.utils.translation import templatize
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as  auth_views
from .forms import LoginForm, ChangePwdForm, ResetPwdForm, SetPwdForm

urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:id>', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plus_cart, name='plus-cart'),
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='remove-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(
        template_name='app/changepassword.html',
        form_class=ChangePwdForm, success_url='/passwordchangedone/'), name='changepassword'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('mobile/', views.mobile, name='mobile'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('laptop/', views.laptop, name='laptop'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('topwear/', views.topwear, name='topwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    
    path('accounts/login/', 
    auth_views.LoginView.as_view(template_name='app/login.html',
    authentication_form=LoginForm), name='login'),
    
    path('passwordchangedone/', 
    auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html',
    ), name='passwordchangedone'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', 
        form_class=ResetPwdForm), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html', form_class=SetPwdForm),
        name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
        name='password_reset_complete'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
