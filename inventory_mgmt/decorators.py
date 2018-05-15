from django.shortcuts import redirect


def check_user_auth(func):

    def check_login(request, *args, **kwargs):
        if request.session.get('email'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')
    return check_login
