from .. import errors
from ..utils import modelutils, cryptoutils
from ..models import User
from ..serializers import user_serializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserDIDResponse(APIView):

    """
    [GET] /api/user/:did
    @PathVariable:  :did    DID URI
    @RequestParam:  nil
    @RequestBody:   nil
    """
    @staticmethod
    def gen_get_response(user_info, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "user_info": user_info,
            },
            status=code,
        )

    def get(self, request, did):
        try:

            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            cookie_did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Get user info
            # Generate serializer
            did = cookie_did if did == "self" else did
            user_obj = User.objects.get(pk=did)

            serializer = None
            if modelutils.is_employee(cookie_did):
                serializer = user_serializer.EmployeeReadableSerializer(user_obj)
            else:
                serializer = user_serializer.EmployerReadableSerializer(user_obj)

            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError(err).gen_response()

        except User.DoesNotExist: # type: ignore
            return errors.AuthorizationFailedError().gen_response()

        # Handle unhandled error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
