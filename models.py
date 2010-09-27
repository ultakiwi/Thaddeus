import datetime, os, sys
import Image

from django.core.files import File
from django.conf import settings
from django.db import models
from markdown import markdown

class Photo(models.Model):
	title = models.CharField(max_length=250,
		help_text='Maximum 250 characters.')
	slug = models.SlugField(unique=True, 
		help_text='Suggested value automatically generated from title. Must be unique.')
	summary = models.TextField(blank=True,
		help_text='An optional summary.')
	summary_html = models.TextField(editable=False, blank=True)
	date = models.DateTimeField(default=datetime.datetime.now)
	image = models.ImageField(upload_to='photos',
		help_text='Maximum resolution 800x600. Larger images will be resized.')
	thumb = models.ImageField(upload_to='photos', editable=False)
		
	class Meta:
		ordering = ['-date']
	def __unicode__(self):
		return self.title
	def save(self, force_insert=False, force_update=False):
		if self.summary:
			self.summary_html = markdown(self.summary)
		super(Photo, self).save(force_insert, force_update)
		if self.image and not self.thumb:
			# Set the thumbnail size and maximum size.
			t_size = 200, 150
			max_size = 800, 600
			# Open the image that was uploaded.
			im = Image.open(settings.MEDIA_ROOT + str(self.image))
			# Compare the image size against the maximum size. If it is greater, the image will be resized.
			if im.size > max_size:
				# Using 'thumbnail', instead of 'resize', keeps the aspect ratio of the image.
				resize = im.thumbnail(max_size)
				resize.save(settings.MEDIA_ROOT + str(self.image))
			# Create the thumbnail and save the path to the database.
			im.thumbnail(t_size)
			im.save(settings.MEDIA_ROOT + os.path.splitext(str(self.image))[0] + ".thumbnail", "JPEG")
			self.thumb = os.path.splitext(str(self.image))[0] + ".thumbnail"
			super(Photo, self).save(force_insert, force_update)
	def get_absolute_url(self):
		return ('thaddeus_photo_detail', (),
			{ 'slug': self.slug })
	get_absolute_url = models.permalink(get_absolute_url)
