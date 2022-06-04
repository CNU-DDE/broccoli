from .. import errors, serializers
from ..utils import cryptoutils, modelutils
from ..models import ClaimData

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ClaimDetailResponse(APIView):

    @staticmethod
    def gen_get_response(detail, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "detail": detail,
            },
            status=code,
        )

    """
    [GET] /api/claim/:claim_id
    @PathVariable:  nil
    @RequestParam:  claim_id    Claim ID
    @RequestBody:   nil
    """
    def get(self, request, claim_id):
        try:

            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Generate serializer
            serializer = None

            # For employee
            if modelutils.is_employee(did):
                serializer = serializers.EmployeeClaimDetailSerializer(
                    ClaimData.objects.filter(pk=claim_id).select_related("issuer"), # type: ignore
                    many=True,
                )

            # For employer
            else:
                serializer = serializers.EmployerClaimDetailSerializer(
                    # Filter only `PENDING(1)` status claims for the employers
                    ClaimData.objects.filter(pk=claim_id, status=1).select_related("owner"), # type: ignore
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
