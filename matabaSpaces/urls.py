
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500, handler403, handler400
from stats import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('park.urls')),
    path('', include('authentication.urls')),
    path('', include('reservation.urls')),
    path('extra/', include('stats.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    
]
urlpatterns += staticfiles_urlpatterns()


admin.site.site_header="🚘🅿matabaSPACES"
admin.site.site_title="mataba"
admin.site.index_title="The SuperAdmin Area of MatabaSPACES"

handler404 = 'stats.views.custom_404_view'
handler500 = 'stats.views.custom_500_view'
handler403 = 'stats.views.custom_403_view'
handler400 = 'stats.views.custom_400_view'