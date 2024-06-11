from __future__ import annotations
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'updated_on', 'created_on', 'content', 'metades', 'status']