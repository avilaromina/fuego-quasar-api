from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from transmission.helpers import get_location, get_message, map_distances
from transmission.serializer import VkBaseSerializer


class TopSecretView(APIView):
    permission_classes = []
    http_method_names = ['post']
    serializer_class = VkBaseSerializer

    def post(self, request, *args, **kwargs):
        valid_ser = self.serializer_class(data=request.data)
        if valid_ser.is_valid():
            satellites = request.data.get('satellites')

            location = get_location(map_distances(satellites))
            if location is None:
                return Response(
                    "The distances not correspond to a valid coordinate.",
                    status.HTTP_400_BAD_REQUEST
                )

            message = get_message([satellite['message'] for satellite in satellites])
            if message is None:
                return Response(
                    "The message cant be display because the all the messages aren't the same.",
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
