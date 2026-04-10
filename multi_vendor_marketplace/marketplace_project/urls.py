from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# Added checkout and success to the imports
from core.views import (
    frontpage, product_detail, signup, 
    add_product, logout_view, checkout, success
)

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Authentication
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Shop & Product Logic
    path('', frontpage, name='frontpage'),
    path('add-product/', add_product, name='add_product'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # --- NEW: Purchase Flow Paths ---
    path('checkout/<int:pk>/', checkout, name='checkout'),
    path('success/', success, name='success'),
]

# Media File Handling (Critical for showing your Product Images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)