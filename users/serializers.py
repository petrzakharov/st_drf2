from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name', 'middle_name', 'phone', 'address')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email'].split('@')[0]
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.username = validated_data['email'].split('@')[0]
        instance.save()
        return super().update(instance, validated_data)

