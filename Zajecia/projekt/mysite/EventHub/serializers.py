from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Event, Enrollment, Comment, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'registered_at']


class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category', 'location', 'date',
            'created_by', 'max_participants', 'current_participants'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'event', 'enrolled_at']

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data['event']
        return Enrollment.objects.create(user=user, event=event)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')  # Ustawienie jako pole tylko do odczytu
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'event', 'user', 'content', 'rating', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data.pop('event')
        return Comment.objects.create(user=user, event=event, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Niepoprawny login lub hasło.")
        return {"user": user}


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ['key', 'user']