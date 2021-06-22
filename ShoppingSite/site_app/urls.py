from django.urls import path
from site_app import views
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from site_app.forms import EmailForForgotPassword, UserSetPasswordForm

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('base_page/', views.base_page),
    path('index_page/', views.index_page),
    #path("login_page/", auth_views.LoginView.as_view(template_name='site_app/login_page.html'), name='login_page'),
    path('login_page/', views.login_page),
    path('user_logout/', views.user_logout),
    path('changepassword_page/', views.changepassword_page),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailForForgotPassword), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('password_reset_done/', views.password_reset_done),



    path('signup_page/', views.signup_page),
    path('myprofile_page/', views.myprofile_page),
    path('userdetail_page/', views.userdetail_page),

    path('product_detail/', views.product_detail, name='product_detail'),

    path('apple_page/', views.apple_page, name='apple_page'),
    path('apple_page/<slug:data>', views.apple_page,  name='apple_data'),

    path('samsung_page/', views.samsung_page, name='samsung_page'),
    path('samsung_page/<slug:data>', views.samsung_page, name='samsung_data'),

    path('oppo_page/', views.oppo_page, name='oppo_page'),
    path('oppo_page/<slug:data>', views.oppo_page, name='oppo_data'),

    path('lapple_page/', views.lapple_page, name='lapple_page'),
    # slug is send for filter mobile to low-high price
    path('lapple_page/<slug:data>', views.lapple_page, name='lapple_data'),

    path('lasus_page/', views.lasus_page, name='lasus_page'),
    path('lasus_page/<slug:data>', views.lasus_page, name='lasus_data'),

    path('lhp_page/', views.lhp_page, name='lhp_page'),
    path('lhp_page/<slug:data>', views.lhp_page, name='lhp_data'),

    path('lg_page/', views.lg_page, name='lg_page'),
    path('lg_page/<slug:data>', views.lg_page, name='lg_data'),

    path('panasonic_page/', views.panasonic_page, name='panasonic_page'),
    path('panasonic_page/<slug:data>', views.panasonic_page, name='panasonic_data'),

    path('sony_page/', views.sony_page, name='sony_page'),
    path('sony_page/<slug:data>', views.sony_page, name='sony_data'),

    path('buy_now/', views.buy_now, name='buy_now'),
    path('cart_page/', views.addtocart_page, name='cart_page'),
    path('show_mycart/', views.show_mycart, name='show_mycart'),
    path('delete/', views.delete),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),

    path('address_page/', views.address_page, name='address_page'),
    path('update/', views.update, name='update'),
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    #path('payment_done/', views.payment_done, name='payment_done'),
    path('order_page/', views.order_page, name='order_page'),
    path('show_order/', views.show_order, name='show_order'),
]
