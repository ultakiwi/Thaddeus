from django.contrib import admin
from thaddeus.models import Photo

class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ['title'] }
	list_display = ('title', 'date')

admin.site.register(Photo, PhotoAdmin)
