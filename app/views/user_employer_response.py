from app.utils.convutils import user_type
from .. import errors
from ..models import User
from ..serializers import UserMinimumSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserEmployerResponse(APIView):

    @staticmethod
    def send_response(employers, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "employers": employers,
            },
            status=code,
        )

    """
    [GET] /api/user/employers
    @PathVariable:  nil
    @RequestParam:  nil
    @RequestBody:   nil
    """
    def get(self, _):
        try:

            # SELECT all employers
            serializer = UserMinimumSerializer(
                User.objects.filter(user_type = user_type(False)),
                many = True,
            )

            return self.send_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError(err).gen_response()

        # Handle unhandled error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
