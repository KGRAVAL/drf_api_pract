from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustUser


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
    current_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        # fields = ('current_password','password', 'password2')
        fields = ('current_password','password', 'password2')
    #
    def validate(self, attrs):
        # current_password = attrs.get('password')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if current_password != self.requ:
            raise serializers.ValidationError('Your current password did not matched')
        else:
            if password != password2:
                raise serializers.ValidationError('Password and confirm  password are not matching')
            user.set_password(password)
            user.save()
            return attrs
