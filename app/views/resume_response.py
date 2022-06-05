from .. import serializers, errors
from ..utils import cryptoutils, modelutils, httputils
from ..models import ResumeData

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

def gen_get_response(resume_list, code=status.HTTP_200_OK, err=None):
    return Response(
        {
            "error": err,
            "resumes": resume_list,
        },
        status=code,
    )

class ResumeResponse(APIView):

    @staticmethod
    def gen_post_response(code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    """
    [POST] /api/resume
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: {
        keystore:           { did: string, walletAddress: string, privKey: string, pubKey: string }
        title:              string
        cover_letter_ids:   []int
        carears:            []string
    }
    """
    def post(self, request):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Check employee
            if not modelutils.is_employee(did):
                raise errors.PermissionDeniedError()

            # Generate VP
            vp = httputils.did_post_req("/ssi/verifiable-presentation", {
                "holderDID": did,
                "holderPriv": request.data["keystore"]["privKey"],
                "verifiableCredentials": request.data["careers"],
            })

            # Generate resume
            content = {
                "cover_letters": request.data["cover_letter_ids"],
                "careers": vp,
            }

            # Generate serializer
            serializer = serializers.ResumeSerializer(data = {
                "owner":    did,
                "title":    request.data["title"],
                "content":  content,
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
    [GET] /api/resume?position=:position_id
    @PathVariable:  nil
    @RequestParam:  position_id      Position ID
    @RequestBody:   nil
    """
    def get(self, request):
        try:
            # Check login
            if "access_token" not in request.COOKIES:
                raise errors.AuthorizationFailedError("Access token not exists")
            did = cryptoutils.verify_JWT(request.COOKIES["access_token"])

            # Generate serializer
            serializer = None

            # For employee
            if modelutils.is_employee(did):

                serializer = serializers.ResumeDisplaySerializer(
                    # Resume owner is myself
                    ResumeData.objects.filter(owner=did), # type: ignore
                    many=True,
                )

            # When employer inquires about the resumes for a position
            elif "position" in request.query_params:

                serializer = serializers.ResumeDisplaySerializer(
                    # Resume verifier is myself
                    # And position id matches
                    ResumeData.objects.filter( # type: ignore
                        verifier=did,
                        position=int(request.query_params["position"]),
                    ),
                    many=True,
                )

            # For employer
            else:
                serializer = serializers.ResumeDisplaySerializer(
                    # Resume verifier is myself
                    ResumeData.objects.filter(verifier=did), # type: ignore
                    many=True,
                )

            # Response
            return gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()

class ResumeAllResponse(APIView):

    """
    [GET] /api/resume/all
    @PathVariable: nil
    @RequestParam: nil
    @RequestBody: nil
    """
    def get(self, _):
        try:

            # Generate serializer
            serializer = serializers.ResumeDisplaySerializer(
                ResumeData.objects.all(), # type: ignore
                many=True,
            )

            # Response
            return gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
