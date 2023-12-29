import jwt
import time
from datetime import datetime, timedelta
from jwt.exceptions import PyJWTError


class Tokenizator:
    ALGORITHM = "HS256"
    access_token_jwt_subject = "access"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
   

    def __init__(self, config, *args, **kwargs):
        self.secret_key = config.SECRET_KEY
        if kwargs.get('expires'):
            self.ACCESS_TOKEN_EXPIRE_MINUTES = kwargs['expires']

    def create_token(self, id: [int, str], *args, **kwargs) -> dict:
        """
        :param user_uid:
        :type user_uid:
        :param username:
        :type username:
        :param email:
        :type email:
        :return: JWT Token
        :rtype: dict
        """
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_expires2 = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"id": id}
        if kwargs:
            data.update(kwargs)

        access_token = self.create_access_token(
                data=data,
                expires_delta=access_token_expires
            )
        refresh_token = self.create_access_token(
                data={"id": id}
            )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_expire": datetime.timestamp(access_token_expires2)
        }

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """
        :param data:
        :type data:
        :param expires_delta:
        :type expires_delta:
        :return: token
        :rtype: string
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire, "sub": self.access_token_jwt_subject})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.ALGORITHM)

    def decode_token(self, token: str) -> str:
        """
        :param token:
        :type token:
        :return: user uuid
        :rtype: str
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])['id']
        except (Exception, jwt.exceptions.ExpiredSignatureError) as error:
            raise Exception(error)
        

class AdvancedJwt:
    def _generate_signed_token(self, signing_key_id, private_key, uri, exp=3600, nbf=None):
        payload = {'uri': uri}
        if exp > 0:
            payload['exp'] = int(time.time()) + exp
        if nbf is not None:
            payload['nbf'] = nbf

        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': signing_key_id}

        try:
            return jwt.encode(payload, private_key, algorithm='RS256', headers=headers)
        except PyJWTError as e:
            raise e

    def generate_signed_token(self, signing_key_id, private_key, uri, exp=3600, nbf=None):
        try:
            return self._generate_signed_token(signing_key_id, private_key, uri, exp, nbf)
        except PyJWTError as e:
            raise e

    def generate_signed_token_for_bucket(self, signing_key, uri=''):
        try:
            return self._generate_signed_token(signing_key['id'], signing_key['private_key'], uri)
        except PyJWTError as e:
            raise e

    def generate_signed_token_for_stream(self, signing_key, uri=''):
        try:
            return self._generate_signed_token(signing_key['id'], signing_key['private_key'], uri)
        except PyJWTError as e:
           raise e
    