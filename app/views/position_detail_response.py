from .. import errors
from ..models import PositionData
from ..serializers import PositionDetailSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PositionDetailResponse(APIView):

    @staticmethod
    def gen_get_response(position, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "position": position,
            },
            status=code,
        )

    """
    [GET] /api/position/:position_id
    @PathVariable:  nil
    @RequestParam:  position_id     Position ID
    @RequestBody:   nil
    """
    def get(self, _, position_id):
        try:

            # Generate serializer
            serializer = PositionDetailSerializer(
                PositionData.objects.filter(pk=position_id).select_related("owner"), # type: ignore
                many=True,
            )

            # Response just one
            if len(serializer.data) == 1:
                return self.gen_get_response(serializer.data[0])
            else:
                return self.gen_get_response({})

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
