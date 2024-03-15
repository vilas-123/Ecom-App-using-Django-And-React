from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from userauths.models import Profile, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        def validate():
            # try:
            #     data['vendor_id'] = data[user].vendor.id
            # except AttributeError:
            #     data['vendor_id'] = 0
            # return data
            pass
        validate()
        token = super().get_token(user)
        print(token)
        token['full_name'] = user.fullname
        token['email'] = user.email
        token['username'] = user.username
        return token

    # def validate(self, data):
    #     try:
    #         data['vendor_id'] = data[user].vendor.id
    #     except AttributeError:
    #         data['vendor_id'] = 0
    #     return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password', 'confirm_password', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password does not match the confirm password."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
        full_name=validated_data['full_name'],
        email=validated_data['email'],
        phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
