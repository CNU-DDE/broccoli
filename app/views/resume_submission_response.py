from .. import serializers, errors
from ..utils import cryptoutils, modelutils
from ..models import ResumeData, PositionData

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ResumeSubmissionResponse(APIView):

    @staticmethod
    def gen_post_response(code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    """
    [POST] /api/resume/submission
    @PathVariable:  nil
    @RequestParam:  nil
    @RequestBody: {
        submit_to:  int
        resume_id:  int
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

            # Get resume
            resume = ResumeData.objects.get( # type: ignore
                pk=request.data["resume_id"],
                owner=did,
            )

            # Get position
            position = PositionData.objects.get(pk=request.data["submit_to"]) # type: ignore

            # Generate serializer
            serializer = serializers.ResumeSerializer(data={
                "owner": did,
                "title": resume.title,
                "content": resume.content,
                "verifier": position.owner.did,
                "position": position.id,
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
