
from js9 import j

def catch_exception_decoration_return(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            jwt=j.clients.itsyouonline.get(instance="main").jwt
            self.ovc_data["_jwt"]=jwt
            return wrapper(self, *args, **kwargs)
    return wrapper