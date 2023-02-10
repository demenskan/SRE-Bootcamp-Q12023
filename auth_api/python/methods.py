import json
import jwt
import hashlib
import mysql.connector
from mysql.connector import Error

# These functions need to be implemented
class Token:

    def generate_token(self, username, password):

        #conectarse a la base de datos y buscar el usuario enviado
        try:
            connection = mysql.connector.connect(host="sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com",
                                                 database="bootcamp_tht",
                                                 user="secret",
                                                 password="jOdznoyH6swQB9sTGdLUeeSrtejWkcw")
            if connection.is_connected():
                #db_Info = connection.get_server_info()
                cursor = connection.cursor()
                sql_query= """Select * from users where username=%s"""
                cursor.execute(sql_query,(username,))
                record = cursor.fetchone()
                if cursor.rowcount < 0:
                    return "user_not_found"
                #si existe, agregarle el 'salt' al password y hashearlo con el SHA512
                pass_hasheado=hashlib.sha512(str(password+record[2]).encode("utf-8")).hexdigest()
                #comparar el resultado con lo que hay en la base
                #si son iguales, devolver el 'role'. Caso contrario, devolver un error http 403
                if pass_hasheado==record[1]:
                    # tomar el 'role', generar la JWT y poner en el payload (contenido) el 'role' encriptado con este secreto: my2w7wjd7yXF64FIADfJxNs1oupTGAuW
                    payload_data = {
                            "role" : record[3]
                            }
                    jwt_secret="my2w7wjd7yXF64FIADfJxNs1oupTGAuW"
                    token=jwt.encode(
                                payload=payload_data,
                                key=jwt_secret
                            )
                    return token
                else:
                    return "X("

        except Error as e:
            return 'Error'

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


class Restricted:

    def access_data(self, authorization):
        #regresar 'you are under protected data' si hay token con el rol definido y la firma coincide con el secret.
        #caso contrario yo creo que devuelve igual un 403
        #return authorization[7:]
        token_entrada=jwt.decode(authorization[7:], key='my2w7wjd7yXF64FIADfJxNs1oupTGAuW', algorithms=['HS256', ])
        #token_dicc=json.loads(token_entrada)
        return token_entrada['role']
