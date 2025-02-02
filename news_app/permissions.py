from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Дает полные права авторизованным пользователям,
    а неавторизованным только чтение.
    """

    def has_permission(self, request, view):
        # Разрешаем только чтение для неавторизованных
        if request.method in permissions.SAFE_METHODS:
            return True
        # Полный доступ для авторизованных
        return request.user and request.user.is_authenticated
