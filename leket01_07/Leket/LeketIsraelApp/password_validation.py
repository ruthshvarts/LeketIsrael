from django.contrib.auth import password_validation
import functools
import gzip
import os
import re
from difflib import SequenceMatcher

from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.translation import gettext as _, ngettext


class MinimumLengthValidator(password_validation.MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(_(
                f"הסיסמה חייבת להיות באורך מינימלי של {self.min_length} תווים לפחות."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class CommonPasswordValidator(password_validation.CommonPasswordValidator):
    DEFAULT_PASSWORD_LIST_PATH = password_validation.CommonPasswordValidator.DEFAULT_PASSWORD_LIST_PATH

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except IOError:
            with open(password_list_path) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("הסיסמה נראית כמו סיסמה נפוצה מדי."),
                code='password_too_common',
            )


class NumericPasswordValidator(password_validation.NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("הסיסמה לא יכולה להיות מספרים בלבד."),
                code='password_entirely_numeric',
            )


class UserAttributeSimilarityValidator(password_validation.UserAttributeSimilarityValidator):
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("הסיסמה דומה מידי ל %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )
