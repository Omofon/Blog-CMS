from django.contrib import admin
from .models import Post

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated_on", "created_on"]
	list_display_links = ["updated_on"]
	list_editable = ["title"]
	list_filter = ["updated_on", "created_on"]

	search_fields = ["title", "content"]
	
	class Meta:
		model = Post
		
admin.site.register(Post, PostModelAdmin)