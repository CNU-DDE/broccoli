from ..models import User
from ..utils import cryptoutils, convutils

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

"""
[POST] /api/user/token
@RequestBody: {
    password:   string,
    keystore:   { did: string, walletAddress: string, privKey: string, pubKey: string }
}
TODO: This might not work due to CORS and CSRF problem
"""
class UserTokenResponse(APIView):

    @staticmethod
    def send_response(code=status.HTTP_200_OK, err=None):
        return Response(
            {
                "error": err,
            },
            status=code,
        )

    def post(self, request):
        try:
            # Get keystore
            keystore = request.data["keystore"]

            # Generate password hash
            password = cryptoutils.hash_dict({
                "password": request.data["password"],
                "keystore": keystore,
            })

            # SELECT 1 FROM user;
            is_user_exists = User.objects.filter(
                identifier = keystore["pubKey"],
                password = password,
            )

            # Validate: User found
            if is_user_exists:
                res = self.send_response()
                res.set_cookie("access-token", cryptoutils.gen_JWT({
                    "identifier": keystore["pubKey"],
                }))
                return res

            # Validate: User not found
            return self.send_response(status.HTTP_401_UNAUTHORIZED, "User not found")

        # Unknown error
        except Exception as err:
            return self.send_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                convutils.error_message(err),
            )
