def assign_user_role(strategy, details, backend, user=None, *args, **kwargs):
    email = details.get('email')

    if user:
        if email.endswith('@gov.tw'):
            user.user_type = 'admin'
        elif 'disadvantage' in email:
            user.user_type = 'disadvantage'
        else:
            user.user_type = 'normal'
        user.save()