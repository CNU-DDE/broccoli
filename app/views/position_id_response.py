from .. import errors
from ..models import PositionData
from ..serializers import PositionDetailSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class PositionIDResponse(APIView):

    """
    [GET] /api/position/:position_id
    @PathVariable:  nil
    @RequestParam:  position_id     Position ID
    @RequestBody:   nil
    """
    @staticmethod
    def gen_get_response(position, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "position": position,
            },
            status=code,
        )

    def get(self, _, position_id):
        try:

            # Generate serializer
            serializer = PositionDetailSerializer(
                PositionData.objects.get(pk=position_id), # type: ignore
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except PositionData.DoesNotExist: # type: ignore
            return errors.NotFoundError().gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
