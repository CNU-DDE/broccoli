from .. import serializers, errors
from ..utils import httputils
from ..models import ResumeData, CLData, User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ResumeDetailResponse(APIView):

    @staticmethod
    def gen_get_response(detail, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "resume": detail,
            },
            status=code,
        )

    @staticmethod
    def serialize_cover_letter_ids(cl_list):
        def serialize(cl_id):
            serializer = serializers.CLListSerializer(
                CLData.objects.filter(pk=cl_id), # type: ignore
                many=True,
            )
            return serializer.data[0]

        return map(serialize, cl_list)

    @staticmethod
    def serialize_careers(vp_list):
        def serialize(obj):
            ret = {}

            # Format issuer
            serializer = serializers.EmployerReadableSerializer(
                User.objects.get(pk=obj["issuer"]["id"]),
            )

            ret["issuer"] = serializer.data

            # Format subject
            ret["subject"] = obj["credentialSubject"]

            return ret

        return map(serialize, vp_list)

    """
    [GET] /api/resume/:resume_id
    @PathVariable:  resume_id   Resume ID
    @RequestParam:  nil
    @RequestBody:   nil
    """
    def get(self, _, resume_id):
        try:

            # Generate serializer
            serializer = serializers.ResumeDetailSerializer(
                    ResumeData.objects.filter(pk=resume_id), # type:ignore
                many=True,
            )

            # A number of response must be 1
            if len(serializer.data) != 1:
                return self.gen_get_response({})

            res_body = serializer.data[0]

            # Format cover letter
            res_body["cover_letters"] = self.serialize_cover_letter_ids(res_body["cover_letters"])

            # Format careers
            try:

                # Get verified presentation
                verified = httputils.did_post_req("/ssi/verified-presentation", {
                    "verifiablePresentation": res_body["careers"],
                })

                # Process & serialize verified presentation
                res_body["careers"] = self.serialize_careers(
                    verified["verifiablePresentation"]["verifiableCredential"],
                )

                # When executed normally
                res_body["career_verified"] = True

            except errors.DIDReqError:
                # When VP verification fails
                res_body["careers"] = None
                res_body["career_verified"] = False

            return self.gen_get_response(res_body)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
