from graphene_django.views import GraphQLView
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTGraphQLView(GraphQLView):
    """GraphQL view that accepts Authorization: Bearer <token> and sets request.user accordingly."""
    def parse_body(self, request):
        # ensure DRF's JWTAuthentication runs to set request.user
        auth = JWTAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                user, validated_token = user_auth_tuple
                request.user = user
        except Exception:
            # leave request.user as-is (anonymous)
            pass
        return super().parse_body(request)
