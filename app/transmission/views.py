from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import (
    SATELLITES,
    SATELLITES_NAMES,
)
from transmission.helpers import (
    clear_tmp_distances,
    get_location,
    get_message,
    get_temp_distances,
    map_distances,
    set_temp_distances,
    validate_is_satellites_are_correct,
)
from transmission.serializer import (
    TopSecretBaseSerializer,
    TopSecretSplitSerializer,
)


class TopSecretView(APIView):
    permission_classes = []
    http_method_names = ['post']
    serializer_class = TopSecretBaseSerializer

    def post(self, request, *args, **kwargs):
        valid_ser = self.serializer_class(data=request.data)
        if valid_ser.is_valid():
            satellites = request.data.get('satellites')

            location = get_location_if_valid(satellites)

            if location is None:
                return Response(
                    "Distances do not match a valid coordinate.",
                    status.HTTP_400_BAD_REQUEST
                )

            message = get_message([satellite['message'] for satellite in satellites])
            if message is None:
                return Response(
                    "Invalid message or format.",
                    status.HTTP_400_BAD_REQUEST
                )

            return Response({
                'position': {
                    'x': location[0],
                    'y': location[1],
                },
                'message': message
            })
        else:
            raise APIException(valid_ser.errors)


class TopSecretSplitView(APIView):
    permission_classes = []
    http_method_names = ['post', 'get']
    serializer_class = TopSecretSplitSerializer

    def post(self, request, *args, **kwargs):
        satellite = kwargs['name']
        if satellite in SATELLITES_NAMES:
            valid_ser = self.serializer_class(data=request.data)
            if valid_ser.is_valid():
                set_temp_distances(
                    satellite.lower(),
                    request.data.get('distance'),
                    request.data.get('message')
                )
                return Response(get_temp_distances([satellite]))
            else:
                raise APIException(valid_ser.errors)
        else:
            raise ValidationError('{} isn\'t a valid sattelite name'.format(satellite))

    def get(self, request, *args, **kwargs):

        satellites = get_temp_distances(SATELLITES.keys())
        location = get_location_if_valid(satellites)

        if location is None:
            return Response(
                "Distances do not match a valid coordinate.",
                status.HTTP_400_BAD_REQUEST
            )

        message = get_message([satellite['message'] for satellite in satellites])
        if message is None:
            return Response(
                "Invalid message or format.",
                status.HTTP_400_BAD_REQUEST
            )

        clear_tmp_distances()

        return Response({
            'position': {
                'x': location[0],
                'y': location[1],
            },
            'message': message
        })


def get_location_if_valid(satellites):
    distances = map_distances(satellites)
    if validate_is_satellites_are_correct(list(distances.keys())):
        return get_location(distances)
    return None
