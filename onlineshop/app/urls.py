from django import urls
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .forms import MyPasswordChangeForm, MyPaasswordResetFrom, MySetPasswordForm
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.home, name='Home'),
    path('product-detail/<int:id>', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('updatecart/', views.update_cart, name='updatecart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
                                                                  form_class=MyPasswordChangeForm), name='changepassword'),


    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'),
         name='password_change_done'),

    path('mobile/', views.mobile, name='mobile'),

    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('airphone/', views.airphone, name='airphone'),
    path('airphone/<slug:data>', views.airphone, name='airphonedata'),
    path('tablet/', views.tablet, name='tablet'),
    path('tablet/<slug:data>', views.tablet, name='tabletdata'),
    path('login/', views.login, name='login'),
    path('logout/', views.handlelogout, name='logout'),
    path('registration/', views.CustomerRegistrationView,
         name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPaasswordResetFrom), name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
