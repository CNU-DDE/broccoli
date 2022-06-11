from app.serializers.CL_serializer import CLDetailSerializer
from .. import errors
from ..utils import cryptoutils, modelutils
from ..models import CLData

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class CoverLetterIDResponse(APIView):

    """
    [GET] /api/cover-letter/:cl_id
    @PathVariable:  :ci_id  Cover letter ID
    @RequestParam:  nil
    @RequestBody:   nil
    """
    @staticmethod
    def gen_get_response(cl, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "cover_letter": cl,
            },
            status=code,
        )

    def get(self, request, cl_id):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employee
            if not modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate serializer
            serializer = CLDetailSerializer(
                    CLData.objects.get(owner = did, pk=cl_id), # type: ignore
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
