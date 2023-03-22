from passlib.context import CryptContext

pass_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password:str):
        return pass_cxt.hash(password)