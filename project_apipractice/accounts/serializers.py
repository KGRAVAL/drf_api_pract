from xml.dom import ValidationErr

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
import base64
from accounts.models import CustUser
from accounts.renderers import RenderUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class UserRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustUser
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # password validation with cpass
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm  password are not matching')
        return attrs

    def create(self, validated_data):
        return CustUser.objects.create_user(**validated_data)


class UserLogin(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustUser
        fields = ['email', 'password']


#       extra_kwargs = {}

class UserData(serializers.ModelSerializer):
    class Meta:
        model = CustUser
        fields = ['id', 'email', 'name']


class ChangePassUser(serializers.ModelSerializer):
    # current_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password1 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model= CustUser
        # fields = ('current_password','password', 'password2')
        fields = ('password1', 'password2')

    def validate(self, attrs):
        # current_password = attrs.get('password')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        # if current_password != self.request.data:
        #     raise serializers.ValidationError('Your current password did not matched')

        if password1 != password2:
            raise serializers.ValidationError('Password and confirm  password are not matching')
        user.set_password(password1)
        user.save()
        return attrs

class SendResetPassEmail(serializers.Serializer):
    email = serializers.EmailField(max_length= 255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if CustUser.objects.filter(email= email).exists():
            # breakpoint()
            user = CustUser.objects.get(email= email)
            uid = user.id
            uid = urlsafe_base64_encode(str(uid).encode('utf-8'))
            token= PasswordResetTokenGenerator().make_token(user)
            token= urlsafe_base64_encode(str(token).encode('utf-8'))
            print(f"Reset token generated : {token}")
            breakpoint()

            lnk_mail= "http://127.0.0.1:8000/base_user/reset_password/"+ uid + '/' + token +'/'
            print(f"Password reset link : {lnk_mail}")

            b = urlsafe_base64_decode(uid).decode('ascii')
            # c = urlsafe_base64_decode(token).decode('ascii')
            # print(b)
            lnk_mail = "http://127.0.0.1:8000/base_user/reset_password/"+ str(urlsafe_base64_decode(uid).decode('ascii')) + '/' + token +'/'
            print(f"Password reset link : {lnk_mail}")

            return attrs
        else:
            return ValidationErr("You have not valid mail id...")
