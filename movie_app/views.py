from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def movie_detail_api_view(request, id):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(data={'error': 'Movie does not found'}, status=status.HTTP_404_NOT_FOUND)
        data = MovieSerializer(movie, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        movie_id = request.data.get('id')
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Movie not found"})
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    elif request.method == 'DELETE':
        movie_id = request.data.get('id')
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Movie not found"})

@api_view(['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        title = request.data.get('title')
        director = request.data.get('director')
        description = request.data.get('description')
        duration = request.data.get('duration')

        movie = Movie.objects.create(
            title=title,
            director=director,
            description=description,
            duration=duration)

        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)


@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')

        director = Director.objects.create(name=name)

        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)


@api_view(['GET', 'DELETE', 'PUT'])
def director_detail_api_view(request, id):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')
        director = Director.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)

    elif request.method == 'DELETE':
        director_id = request.data.get('id')
        try:
            director = Director.objects.get(id=director_id)
            director.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Director not found"})
    elif request.method == 'PUT':
        director_id = request.data.get('id')
        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Director not found"})

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        movie = request.data.get('movie')
        text = request.data.get('text')
        stars = request.data.get('stars')

        review = Review.objects.create(
            movie=movie,
            text=text,
            stars=stars)

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)

@api_view(['GET', 'DELETE', 'PUT'])
def review_detail_api_view(request, id):
    if request.method == 'GET':
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(data={'error': 'Review does not found'}, status=status.HTTP_404_NOT_FOUND)
        data = ReviewSerializer(review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)


    elif request.method == 'PUT':
        review_id = request.data.get('id')
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review_id = request.data.get('id')
        review =Review.objects.get(id=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)