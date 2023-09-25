from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.model.user import CustomUser
from . import serializers
from .. import pagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import Group, Permission, User


class LogInView(TokenObtainPairView):
    """separate login api for admin panel || ADMIN PANEL UCHUN ALOHIDA LOGIN API"""
    @classmethod
    def get_extra_actions(cls):
        return []

    # @login_required(login_url='/account/login/')
    def post(self, request, *args, **kwargs):
        # try:
            username = request.data.get('username', None) or request.query_params.get('username', None)
            password = request.data.get('password', None) or request.query_params.get('password', None)
            if password and username:
                try:
                    user = User.objects.get(username=username)
                except Exception:
                    # Handle the case when the user does not exist
                    return Response("Foydalanuvchi topilmadi!", status=status.HTTP_401_UNAUTHORIZED)
                if not user.check_password(password):
                    return Response("Foydalanuvchi topilmadi!", status=status.HTTP_401_UNAUTHORIZED)
                if user:
                    # user.is_active = True
                    # user.update_last_login()
                    # user.save()
                    refresh = TokenObtainPairSerializer().get_token(user)
                    user_permission, data, group_data = [], {}, []
                    for item in user.get_all_permissions():
                        user_permission.append(item[item.index('.') + 1:])
                    for group in user.groups.all():
                        group_data.append(group.name)

                    data['access'] = str(refresh.access_token)
                    data['refresh'] = str(refresh)
                    data['first_name'] = user.first_name
                    data['last_name'] = user.last_name
                    # data['language_name'] = user.language.name if user.language else None
                    # data['language_code'] = user.language.abbreviation if user.language else None
                    # data['language'] = user.language.id if user.language else None
                    # data['state_id'] = user.state.id if user.state else None
                    data['username'] = user.username
                    # data['organization'] = user.organization.id if user.organization else None
                    # data['organization_name'] = user.organization.name if user.organization else None
                    data['roles'] = group_data
                    data['permissions'] = user_permission
                    return Response(data=data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     send_message(e)
        # return Response(username_or_password_error_for_user_login.get('uz_cyrl'), status=status.HTTP_401_UNAUTHORIZED)

        # except Exception:
        #     pass
        # return Response("Foydalanuvchi topilmadi!", status=status.HTTP_401_UNAUTHORIZED)


class UserView(viewsets.ModelViewSet):
    """separate user api for admin panel || ADMIN PANEL UCHUN ALOHIDA USER API"""
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    # pagination_class = pagination.DefaultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)


class GroupView(viewsets.ModelViewSet):
    """separate role api for admin panel || ADMIN PANEL UCHUN ALOHIDA ROLE API"""
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    # pagination_class = pagination.DefaultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)


class PermissionView(viewsets.ModelViewSet):
    """separate permission api for admin panel || ADMIN PANEL UCHUN ALOHIDA PERMISSION API"""
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    pagination_class = pagination.VotePagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
