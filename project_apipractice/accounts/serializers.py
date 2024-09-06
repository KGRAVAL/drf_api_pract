from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from accounts.utils import Util
from accounts.models import CustUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
            token= PasswordResetTokenGenerator().make_token(user)
            print(f"Reset token generated : {token}")
            uid= urlsafe_base64_encode(str(uid).encode('utf-8'))
            token= urlsafe_base64_encode(str(token).encode('utf-8'))
            lnk_mail= "http://127.0.0.1:8000/base_user/reset_password/"+ str(uid) + '/' + token +'/'
            # lnk_mail= urlsafe_base64_encode(str(lnk_mail).encode('utf-8'))
            print(f"Password reset link encoded : {lnk_mail}")
            # lnk_mail = urlsafe_base64_decode(lnk_mail).decode('ascii')
            # print(f"Password reset link decoded : {lnk_mail}")

            body= f"Your reset password link is ...\n {lnk_mail}"

            data= {
                'subject': 'Reset Password link',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs

class UserResetPass(serializers.Serializer):

    password1 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model= CustUser
        fields = ('password1', 'password2')

        def validate(self, attrs):
            password1= attrs.get('password1')
            password2= attrs.get('password2')
            breakpoint()
            uid= self.context.get('uid')
            token= self.context.get('token')

            if password1 != password2:
                raise serializers.ValidationError('Password and confirm  password are not matching')

            uid = urlsafe_base64_decode(uid).decode('ascii')
            token = urlsafe_base64_decode(token).decode('ascii')
            user = CustUser.objects.get(id= uid)

            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password1)
                user.save()
                return attrs
            else:
                raise ValidationError("Token is not valid now !!")

