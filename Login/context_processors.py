from models import UserWallet

def get_user_wallet(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        print UserWallet.objects.filter(user=request.user).first().credit
        return {'usrwlt':UserWallet.objects.get(user=request.user)}
    else:
        return {'usrwil':UserWallet()}