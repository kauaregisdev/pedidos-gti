from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def validate_name(self, value):
        if not all(c.isalpha() or c.isspace() for c in value):
            raise serializers.ValidationError('O nome deve conter apenas letras e espaços.')
        return value

    def validate_password(self, value):
        if ' ' in value:
            raise serializers.ValidationError('A senha não pode conter espaços.')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def validate_name(self, value):
        if not all(c.isalpha() or c.isspace() for c in value):
            raise serializers.ValidationError('O nome deve conter apenas letras e espaços.')
        return value

    def validate_password(self, value):
        if ' ' in value:
            raise serializers.ValidationError('A senha não pode conter espaços.')
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at']
