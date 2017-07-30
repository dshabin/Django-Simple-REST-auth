from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'password' ,'email', 'is_staff')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    ''' Remove from serializer
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    '''
    class Meta:
        model = UserProfile
        fields = (
        'url',
        'is_identity_verified',
        'telephone',
        'id_card_img_address',
        'username',
        'firstname_lastname',
        'email_address',
        'is_email_verified',
        'home_telephone',
        'is_home_telephone_verified',
        'card_number',
        'address',
        )
