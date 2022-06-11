from .. import errors
from ..utils import cryptoutils, modelutils
from ..models import PositionData
from ..serializers import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
    def gen_get_response(pos_list, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "positions": pos_list,
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
        "employment_period":        string
        "working_time":             string
        "payment_interval_type":    string
        "payment_per_interval":     string
        "hiring_number":            string
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
                "employment_period":        request.data["employment_period"],
                "working_time":             request.data["working_time"],
                "payment_interval_type":    request.data["payment_interval_type"],
                "payment_per_interval":     request.data["payment_per_interval"],
                "hiring_number":            request.data["hiring_number"],
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
    [GET] /api/position
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: nil
    """
    def get(self, request):
        try:
            # Ignore unused
            _ = request

            # Generate serializer
            serializer = PositionMinimumSerializer(
                PositionData.objects.all().select_related("owner"), # type: ignore
                many=True,
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()

class PositionIDResponse(APIView):

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
                PositionData.objects.get(pk=position_id), # type: ignore
            )
            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
