from ..serializers import CLSerializer
from ..utils import cryptoutils, modelutils
from .. import errors

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CoverLetterResponse(APIView):

    @staticmethod
    def gen_post_response(code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    """
    [POST] /api/cover-letter
    """
    def post(self, request):
        try:
            # Check login
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employee
            if not modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate serializer
            serializer = CLSerializer(data = {
                "owner": did,
                "title": request.data["title"],
                "content": request.data["cover-letter"],
            })

            # Validation
            if not serializer.is_valid():
                raise errors.ClientFaultError(serializer.errors)

            # Response
            serializer.save()
            return self.gen_post_response()

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError(err).gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
