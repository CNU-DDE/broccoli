from .. import errors, serializers
from ..utils import cryptoutils, modelutils, httputils, convutils
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

    @staticmethod
    def gen_patch_response(code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
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

    """
    [PATCH] /api/claim/:claim_id
    @PathVariable: nil
    @RequestParam: claim_id     Claim ID
    @RequestBody: {
        status: int
        keystore: { did: string, walletAddress: string, privKeyL string, pubKey: string } | null
    }
    """
    def patch(self, request, claim_id):
        try:

            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            issuer_did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employer
            if modelutils.is_employee(issuer_did):
                raise errors.PermissionDeniedError()

            # Get requested values
            new_status = request.data["status"]
            keystore = request.data["keystore"]

            # Get claim
            claim_obj = ClaimData.objects.get(pk=claim_id) #type: ignore
            claim_data = serializers.ClaimSerializer(claim_obj).data

            # Patch status to `ACCEPTED(2)` and generate VC
            if int(new_status) == 2:

                # Get VC
                vc = httputils.did_post_req('/ssi/verifiable-credential', {
                    "holderDID":    claim_data["owner"],
                    "claim":        claim_data["content"],
                    "issuerDID":    keystore["did"],
                    "issuerPriv":   keystore["privKey"],
                })

                # Get encrypted VC
                # For safety, a generated VC is stored with SECP256K1 algorithm,
                # which is used by Ethereum.
                enc_vc = cryptoutils.secp256k1_encrypt(
                    convutils.public_key(claim_data["owner"]),
                    vc,
                )

                # Generate serializer
                serializer = serializers.ClaimSerializer(
                    claim_obj,
                    data={
                        "status":       new_status,
                        "encrypted_vc": enc_vc,
                    },
                    partial=True,
                )

                # Validation
                if not serializer.is_valid():
                    raise errors.ClientFaultError(serializer.errors)

                # Response
                serializer.save()
                return self.gen_patch_response()

            # Patch status to `REJECTED(3)`
            else:

                # Generate serializer
                serializer = serializers.ClaimSerializer(
                    claim_obj,
                    data={
                        "status": new_status,
                        "encrypted_vc": None,
                    },
                    partial=True,
                )

                # Validation
                if not serializer.is_valid():
                    raise errors.ClientFaultError(serializer.errors)

                # Response
                serializer.save()
                return self.gen_patch_response()

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError("Wrong sign in form").gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
