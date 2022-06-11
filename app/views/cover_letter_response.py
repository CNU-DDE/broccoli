from .. import errors
from ..utils import cryptoutils, modelutils
from ..models import CLData
from ..serializers import CLSerializer, CLMinimumSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class CoverLetterResponse(APIView):

    """
    [POST] /api/cover-letter
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: {
        title:          string,
        cover-letter:   string
    }
    """
    @staticmethod
    def gen_post_response(code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    def post(self, request):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employee
            if not modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate serializer
            serializer = CLSerializer(data = {
                "owner": did,
                "title": request.data["title"],
                "content": request.data["cover_letter"],
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

    """
    [GET] /api/cover-letter
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: nil
    """
    @staticmethod
    def gen_get_response(cl_list, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "cover_letters": cl_list,
            },
            status=code,
        )

    def get(self, request):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employee
            if not modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate serializer
            serializer = CLMinimumSerializer(
                CLData.objects.filter(owner = did), # type: ignore
                many=True
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
