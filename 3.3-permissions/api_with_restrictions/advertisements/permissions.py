from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user_ = str(request.user)
        # print(user_, type(user_))
        if user_ == 'admin':
            return True
        elif view.action == 'partial_update' and request.user != obj.creator:
            # raise ValidationError({"non_field_errors": ["Вы не можете менять чужой заказ"]})
            raise ValidationError("Вы не можете менять чужой заказ")

        return request.user == obj.creator
