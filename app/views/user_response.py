from ..serializers import UserSerializer
from ..utils import httputils, cryptoutils, convutils
from ..errors import DIDReqError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

"""
[POST] /api/user
@RequestBody: {
    password:       string,
    isEmployee:     bool,
    displayName:    string,
    birth:          string | null,
    address:        string,
    contact:        string,
    email:          string
}
"""
class UserResponse(APIView):

    @staticmethod
    def send_response(keystore, code=status.HTTP_201_CREATED, err=None):
        return Response(
            {
                "error": err,
                "keystore": keystore,
            },
            status=code,
        )

    def post(self, request):
        try:
            # Get keystore
            keystore = httputils.did_get_req('/ssi/did')

            # Generate password hash
            password = cryptoutils.hash_dict({
                "password": request.data["password"],
                "keystore": keystore,
            })

            # Generate serializer
            serializer = UserSerializer(data = {
                "identifier": keystore["did"],
                "password": password,
                "user_type": convutils.user_type(request.data["isEmployee"]),
                "display_name": request.data["displayName"],
                "birth": request.data["birth"],
                "address": request.data["address"],
                "contact": request.data["contact"],
                "email": request.data["email"],
            })

            # Validation & Response
            if serializer.is_valid():
                serializer.save()
                return self.send_response(keystore)
            return self.send_response(None, status.HTTP_400_BAD_REQUEST, serializer.errors)

        # Known error
        except DIDReqError as err:
            return self.send_response(None, status.HTTP_400_BAD_REQUEST, err.message)

        except KeyError as err:
            return self.send_response(None, status.HTTP_400_BAD_REQUEST, "Wrong sign in form")

        # Unknown error
        except Exception as err:
            return self.send_response(
                None,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                convutils.error_message(err),
            )
