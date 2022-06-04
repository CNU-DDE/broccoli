from .. import errors
from ..utils import httputils, cryptoutils, convutils
from ..serializers import UserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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

    """
    [POST] /api/user
    @PathVariable: nil
    @RequestParam: nil
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
                "did": keystore["did"],
                "password": password,
                "user_type": convutils.user_type(request.data["isEmployee"]),
                "display_name": request.data["displayName"],
                "birth": request.data["birth"],
                "address": request.data["address"],
                "contact": request.data["contact"],
                "email": request.data["email"],
            })

            # Validation
            if not serializer.is_valid():
                raise errors.ClientFaultError(serializer.errors)

            # Response
            serializer.save()
            return self.send_response(keystore)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError("Wrong sign in form").gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
