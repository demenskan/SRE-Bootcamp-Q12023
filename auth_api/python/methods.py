import json
import jwt
import hashlib
import mysql.connector
from mysql.connector import Error

# These functions need to be implemented
class Token:

    def generate_token(self, username, password):

        #connect to database and search for the submitted user
        try:
            connection = mysql.connector.connect(host="sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com",
                                                 database="bootcamp_tht",
                                                 user="secret",
                                                 password="jOdznoyH6swQB9sTGdLUeeSrtejWkcw")
            if connection.is_connected():
                cursor = connection.cursor()
                sql_query= """Select * from users where username=%s"""
                cursor.execute(sql_query,(username,))
                record = cursor.fetchone()
                if cursor.rowcount < 0:
                    return "user_not_found"
                #if the user exists, add the salt to the password & hash it with SHA512
                pass_hasheado=hashlib.sha512(str(password+record[2]).encode("utf-8")).hexdigest()
                #compare the result with the content on the database
                #if they're equal, returns the content of 'role'. Otherwise returns http 403 error
                if pass_hasheado==record[1]:
                    # put the role encrypted with the secret inside the payload section and generate the JWT
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
        # take the token. If there's a defined role & the signature matches the secret, returns 'you are under protected data'
        # Otherwise returns a 403 error
        try:
            #For http header calls
            if (authorization[0:6] == 'Bearer') :
                token_entrada=jwt.decode(authorization[7:], key='my2w7wjd7yXF64FIADfJxNs1oupTGAuW', algorithms=['HS256', ])
            #for unittest
            else:
                token_entrada=jwt.decode(authorization, key='my2w7wjd7yXF64FIADfJxNs1oupTGAuW', algorithms=['HS256', ])

            accepted_roles= ['admin', 'editor', 'viewer' ]
            #here is where each role can have a different business logic
            if token_entrada['role'] in accepted_roles:
                return "You are under protected data"
            else:
                return "Unauthorized"
        except Exception as e:
            return str(e)


