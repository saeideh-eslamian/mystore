def check_login(request):
    user = request.user
    is_logged_in = user.is_authenticated
    if is_logged_in:
        first_name = user.first_name
    else:
        first_name =""    
    return {
        'is_logged_in': is_logged_in,
        'first_name':first_name ,
            }