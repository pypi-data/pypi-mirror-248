# Django Rest Framework
from rest_framework import serializers

# App
from creta.models import ApiHistory, NFTHistory, NFT


# Classes
class NFTSerializer(serializers.ModelSerializer):

    class Meta:
        model = NFT
        fields = ['id', 'token_id', 'request_id',
                  'name', 'address', 'nft_type', 'attributes',
                  'image_url', 'animation_url', 'external_url', 'extra_url',
                  'created_at', 'updated_at']


class NftStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = NFT
        fields = ('request_id',)


class NFTHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NFTHistory
        fields = ['id', 'nft', 'type', 'title', 'created_at', 'updated_at']


class ApiHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiHistory
        fields = ['id', 'title', 'method', 'url', 'headers', 'request', 'response', 'error', 'created_at', 'updated_at']