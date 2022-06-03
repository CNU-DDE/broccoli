from ..serializers import PositionSerializer
from ..utils import cryptoutils, modelutils
from .. import errors
from ..models import CLData

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PositionResponse(APIView):

    @staticmethod
    def gen_post_response(code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    @staticmethod
    def gen_get_response(cl_list, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "cover-letters": cl_list,
            },
            status=code,
        )

    """
    [POST] /api/position
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: {
        "title":                    string
        "content":                  string
        "employment-period":        string
        "working-time":             string
        "payment-interval-type":    string
        "payment-per-interval":     string
        "hiring-number":            string
    }
    """
    def post(self, request):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employer
            if modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate serializer
            serializer = PositionSerializer(data = {
                "owner": did,
                "title":                    request.data["title"],
                "content":                  request.data["content"],
                "employment_period":        request.data["employment-period"],
                "working_time":             request.data["working-time"],
                "payment_interval_type":    request.data["payment-interval-type"],
                "payment_per_interval":     request.data["payment-per-interval"],
                "hiring_number":            request.data["hiring-number"],
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
            serializer = CLListSerializer(
                CLData.objects.filter(owner = did),
                many=True
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
