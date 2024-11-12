from rest_framework import serializers
from .models import Movie, Director, Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.ModelSerializer
    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, obj):
        return obj.movie_set.count()

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    class Meta:
        model = Review
        fields = 'id text stars movie_title'.split()
