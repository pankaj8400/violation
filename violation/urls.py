# violation/urls.py


from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('no-violation/', views.no_violation, name='no_violation'),
    path('generate-report/', views.generate_pdf, name='generate_pdf'),
    path('generate-record/', views.generate_record, name='generate_record'),
    path('view-violations/', views.view_violations, name='view_violations'),
    path('settings/', views.user_settings, name='help'),
    # path('generate-record-by-camera/', views.generate_record_by_camera, name='generate_record_by_camera'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('logout/', views.logout_view, name='logout'),
    
]
    




# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('no_violation/', views.no_violation, name='no_violation'),
#     path('report_page/', views.report_page, name='report_page'),  # Add this line
# ]
