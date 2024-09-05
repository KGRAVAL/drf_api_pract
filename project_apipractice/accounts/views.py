from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.renderers import RenderUser
from accounts.serializers import UserRegister, UserLogin, UserData, ChangePassUser


class UserRegistrationView(APIView):

    def post(self, request):
        render_classes = [RenderUser]
        serializer = UserRegister(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(data={'token': token, 'error': serializer.errors, 'msg': 'Registration successes'},
                            status=status.HTTP_201_CREATED)
        return Response(data={'msg': 'Registration did not completed'},
                        status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     return Response({'msg':'Registration successes'})
    #     ('error': serializer.errors)


class UserLoginView(APIView):
    def post(self, request):
        render_classes = [RenderUser]
        serializer = UserLogin(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    'token': token,
                    'msg': 'Login successes'},
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors': {'non_field error': ['Email or password is incorrect']}},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserProfileView(APIView):
    render_classes = [RenderUser]
    permission_classes = [IsAuthenticated]

    def get(self, request, formate=None):
        serializer = UserData(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserChangePass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, formate=None):
        render_classes = [RenderUser]
        serializer = ChangePassUser(data=request.data, context={'user': request.data})



