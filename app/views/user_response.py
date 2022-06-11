from .. import errors
from ..utils import httputils, cryptoutils, convutils
from ..models import User
from ..serializers import UserSerializer, UserMinimumSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class UserResponse(APIView):

    @staticmethod
    def gen_post_response(keystore, code=status.HTTP_201_CREATED, err=None):
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
        is_employee:    bool,
        display_name:   string,
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
                "user_type": convutils.user_type(request.data["is_employee"]),
                "public_key": keystore["pubKey"],
                "wallet_address": keystore["walletAddress"],
                "display_name": request.data["display_name"],
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
            return self.gen_post_response(keystore)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError("Wrong sign in form").gen_response()

        # Unknown error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()

    @staticmethod
    def gen_get_response(employers, code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
                "users": employers,
            },
            status=code,
        )

    """
    [GET] /api/user?type=:user_type
    @PathVariable:  nil
    @RequestParam:  nil
    @RequestBody:   nil
    """
    def get(self, request):
        try:

            # SELECT all employers
            qp = request.query_params
            users = None

            if "type" in qp:
                users = User.objects.filter(user_type = int(qp["type"]))
            else:
                users = User.objects.all()

            serializer = UserMinimumSerializer(
                users,
                many = True,
            )

            return self.gen_get_response(serializer.data)

        # Handle all known error
        except errors.BaseError as err:
            return err.gen_response()

        except KeyError as err:
            return errors.ClientFaultError(err).gen_response()

        # Handle unhandled error
        except Exception as err:
            return errors.UnhandledError(err).gen_response()
