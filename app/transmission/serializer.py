from rest_framework import serializers


class VkObjectSerializer(serializers.Serializer):
    """Object serializer"""
    name = serializers.ChoiceField(choices=('kenobi', 'skywalker', 'sato'))
    distance = serializers.DecimalField(max_digits=None, decimal_places=2)
    message = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        max_length=25,
    )


class VkBaseSerializer(serializers.Serializer):
    """Base serializer"""
    satellites = serializers.ListField(
        child=VkObjectSerializer(),
        allow_empty=False,
        min_length=3,
        max_length=3
    )
