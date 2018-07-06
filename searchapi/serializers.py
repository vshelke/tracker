from rest_framework import serializers
from searchapi.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'login', 'thumbnail', 'fullname', 'email', 'location', 'created', 'followers', 'languages' )
