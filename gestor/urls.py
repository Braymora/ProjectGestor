from django.urls import path

from . import views

urlpatterns = [
    path('',views.Login,name='login'),
    path('project/administrator',views.inicio_administrador,name='inicio_administrator'),
    path('project/asignar/new',views.asignar,name='asignar'),
    path('project/manager/<str:id_gerente>/', views.inicio_gerente, name='inicio_manager'),
    path('project/new/<str:codigo>',views.nuevoproyecto,name='nuevoproyecto'),
    
    # project 
    path('project/project/<str:codigo>/',views.proyecto,name='project'),
    #! falta kanbas rama test 
    path('project/project/<str:codigo>/risks/',views.riesgos,name='riesgos'), 
    path('project/project/<str:codigo>/risks/new',views.nuevomatriz,name='nuevomatriz'), 
    
    path('project/project/<str:codigo>/lessons/',views.leccionesprojec,name='leccionesprojec'), 
    path('project/project/<str:codigo>/lessons/all',views.leccionesprojecall,name='leccionesprojecall'),
    path('project/project/<str:codigo>/lessons/new',views.nuevalencion,name='nuevalencion'),
    
    path('project/project/<str:codigo>/costs/',views.costos,name='costos'), 
    path('project/project/<str:codigo>/costs/new',views.nuevocosto,name='nuevocosto'), 
    
    path('project/project/<str:codigo>/documentation/',views.docu,name='docu'), 
    path('project/project/<str:codigo>/documentation/new',views.nuevodocu,name='nuevodocu'), 
    
    
    
    
    
    ## server 
    path('logout/', views.Logout, name='logout'),
]