from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, views
from .serializers import UserCreateSerializer, UserVerificationSerializer, User
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password)

    user.generate_verification_code()

    return Response(data={'user_id': user.id, 'verification_code': user.verification_code},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(data={'error': 'User not valid'}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': f'User created. Verification code sent to {user.username}.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerificationView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
