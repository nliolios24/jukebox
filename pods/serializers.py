from rest_framework import serializers

from authentication.models import Account
from pods.models import Pod
from songs.models import Song

class PodSerializer(serializers.ModelSerializer):

    host = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=Account.objects.all()
    )

    members = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='username',
        queryset=Account.objects.all()
    )

    songs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id',
    )
    
    
    class Meta:
        model = Pod
        fields = (
            'id',
            'name',
            'host',
            'members',
            'songs',
        )