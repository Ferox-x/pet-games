from django.contrib.auth import get_user_model
User = get_user_model()


class Profile:
    @staticmethod
    def post_update_or_create_image(image: str, request) -> None:
        User.objects.update_or_create(
            id=request.user.id,
            defaults={
                'id': request.user.id,
                'image': image
            }
        )
