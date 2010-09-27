from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from thaddeus.models import Photo

photo_info = { 'queryset': Photo.objects.all() }

urlpatterns = patterns('',
	url(r'^$', object_list, dict(photo_info, paginate_by=20), name='thaddeus_photo_list'),
	url(r'^(?P<slug>[-\w]+)/$', object_detail, photo_info, name='thaddeus_photo_detail'),
)
