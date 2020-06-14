import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import check_password

class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least 1 symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "A sua senha deve conter pelo menos 1 destes simbolos:" +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

class InvalidPasswordReused:

    def validate(self, password, user=None):
        if user.previous_password:
            if check_password(password, user.previous_password):
                raise ValidationError("A nova senha não pode ser igual a antiga.")
        return None


    def get_help_text(self):
        return "A nova senha não pode ser igual a antiga."