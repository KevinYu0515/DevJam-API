import jwt
from django.conf import settings
from django.http import JsonResponse

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

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.jwt_payload = payload
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.jwt_payload = None
        
        response = self.get_response(request)
        return response