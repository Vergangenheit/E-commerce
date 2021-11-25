from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from .models import UserBase
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: UserBase, timestamp: int):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()
