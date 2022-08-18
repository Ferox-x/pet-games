from django.contrib.auth import get_user_model
User = get_user_model()


class Profile:
    """Базовый класс профиля."""
    @staticmethod
    def post_update_or_create_image(image: str, request) -> None:
        """Обновляет или создает новое изображение в базе данных."""
        User.objects.update_or_create(
            id=request.user.id,
            defaults={
                'id': request.user.id,
                'image': image
            }
        )
