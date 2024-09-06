from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.renderers import RenderUser
from accounts.serializers import UserRegister, UserLogin, UserData, ChangePassUser, SendResetPassEmail, UserResetPass


class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegister(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(data={'token': token, 'error': serializer.errors, 'msg': 'Registration successes'},
                            status=status.HTTP_201_CREATED)
        return Response(data={'msg': 'Registration did not completed'},
                        status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    # @staticmethod
    def post(self, request):
    # def post(request):
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
    render_classes = [RenderUser]
    permission_classes = [IsAuthenticated]

    def post(self, request, formate=None):
        serializer = ChangePassUser(data=request.data, context={'user': request.user})
        print(request.user)
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password change success !!'
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ResetPassEmail(APIView):
    render_classes = [RenderUser]

    def post(self, request, formate= None):
        serializer = SendResetPassEmail(data= request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Link to reset password sent in mail'
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ResetUserPass(APIView):
    render_classes = [RenderUser]

    def post(self, request, uid, token, format= None):
        serializer= UserResetPass(data= request.data, context={
            'uid':uid, 'token': token
        })
        if serializer.is_valid(raise_exception=True):
            return Response({
                'msg': 'Password Reset link send. Check your Email...'
            }, status= status.HTTP_200_OK)
        return Response(serializer.errors, {
            'msg': 'Password Reset Email system faced issue to send link...'
        }, status= status.HTTP_400_BAD_REQUEST)



