from ..serializers import CLSerializer
from ..utils import cryptoutils, convutils
from ..errors import JWTValidationError

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

            # Generate serializer
            serializer = CLSerializer(data = {
                "owner": did,
                "title": request.data["title"],
                "content": request.data["cover-letter"],
            })

            # Validation & response
            if serializer.is_valid():
                serializer.save()
                return self.gen_post_response()
            return self.gen_post_response(status.HTTP_400_BAD_REQUEST, serializer.errors)

        # Handled error
        except JWTValidationError as err:
            return self.gen_post_response(err.status_code, err.message)

        # Unknown error
        except Exception as err:
            return self.gen_post_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                convutils.error_message(err),
            )
