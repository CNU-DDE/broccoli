from .. import errors
from ..utils import httputils, modelutils
from ..models import User
from ..serializers.user_serializer import EmployeeReadableSerializer, EmployerReadableSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserDIDResponse(APIView):

    @staticmethod
    def gen_get_response(user_info, did_doc, code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
                "user_info": user_info,
                "did_doc": did_doc,
            },
            status=code,
        )

    """
    [GET] /api/user/:did
    @PathVariable:  :did    DID URI
    @RequestParam:  nil
    @RequestBody:   nil
    """
    def get(self, _, did):
        try:

            # Get user info
            # Generate serializer
            serializer = None
            if modelutils.is_employee(did):
                serializer = EmployeeReadableSerializer(
                    User.objects.get(pk=did),
                )
            else:
                serializer = EmployerReadableSerializer(
                    User.objects.get(pk=did),
                )

            return self.gen_get_response(
                serializer.data,
                httputils.did_get_req("/ssi/did-document/" + did),
            )

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError(err).gen_response()

        # Handle unhandled error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
