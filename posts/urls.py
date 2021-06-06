from django.contrib import admin
from django.urls import path,include
from  .views import index,postupload,like

urlpatterns = [
  #  path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('uploadpost', postupload, name='uploadpost'),
 #   path('like/<uuid:id>',like(id),name='like')
    path('<uuid:post_id>/', like, name ='postlike'),
  #  path('postdetails',postdetails,name='postdetails')

]