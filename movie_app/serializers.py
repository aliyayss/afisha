from rest_framework import serializers
from .models import Movie, Director, Review
from rest_framework.exceptions import ValidationError

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=100)
    director = serializers.ListField(child=serializers.CharField(required=True, min_length=1, max_length=100))
    description = serializers.CharField( min_length=1, max_length=350)
    duration = serializers.IntegerField( min_value=1, max_value=360)

    def validate_director(self, directors):

        existing_directors = Director.objects.filter(id__in=directors)
        if len(existing_directors) != len(directors):
            raise ValidationError('One or more directors do not exist!')
        return directors

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, obj):
        return obj.movie_set.count()

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=100)
    movies = serializers.ListField(child=serializers.IntegerField())

    def validate_movies(self, movies):
        existing_movies = Movie.objects.filter(id__in=movies)
        if len(existing_movies) != len(movies):
            raise ValidationError('One or more movies do not exist!')
        return movies

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    class Meta:
        model = Review
        fields = 'id text stars movie_title'.split()

class ReviewValidateSerializer(serializers.Serializer):
    movie = serializers.IntegerField()
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(required=False, max_length=1000)

    def validate_movie(self, movie):
        if not Movie.objects.filter(id=movie).exists():
            raise ValidationError("The specified movie does not exist.")
        return movie


