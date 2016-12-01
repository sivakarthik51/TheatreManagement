from models import UserWallet
from Establishments.models import Establishment

def get_user_wallet(request):

    if request.user.is_authenticated and not request.user.is_anonymous and request.user.groups.filter(name='NormalUser').exists():
        try:
            if UserWallet.objects.get(user=request.user) is not None:
                return {'usrwlt':UserWallet.objects.get(user=request.user)}
        except:
            pass
    else:
        return {'usrwlt':None}

def get_user_role(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Establishment').exists() and not request.user.is_anonymous:
        return {'role':Establishment.objects.get(user=request.user).name}
    else:
        return {'role':None}

def isEstablishment(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Establishment').exists() and not request.user.is_anonymous:
        return {'isEstablishment':True}
    else:
        return {'isEstablishment':False}