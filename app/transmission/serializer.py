from rest_framework import serializers

from .constants import SATELLITES_NAMES


class TopSecretSplitSerializer(serializers.Serializer):
    """Top Secret Split Serializer"""
    distance = serializers.DecimalField(max_digits=None, decimal_places=2)
    message = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        max_length=25,
    )


class TopSecretObjectSerializer(TopSecretSplitSerializer):
    """Top Secret API object serializer"""
    name = serializers.ChoiceField(choices=(SATELLITES_NAMES))


class TopSecretBaseSerializer(serializers.Serializer):
    """Top Secret API base serializer"""
    satellites = serializers.ListField(
        child=TopSecretObjectSerializer(),
        allow_empty=False,
        min_length=3,
        max_length=3
    )
