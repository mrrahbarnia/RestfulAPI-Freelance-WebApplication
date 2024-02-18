import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def phone_validator(phone_number):
    if len(phone_number) != 11:
        raise ValidationError(
            _('The length of phone number must be exact 11 digits.'),
            code='Value_Error'
        )

def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include numbers.'),
            code='password_must_include_numbers'
        )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include letters.'),
            code='password_must_include_letters'
        )

def special_character_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _('Password must include special characters.'),
            code='password_must_include_special_char'
        )

def profile_image_size_validator(file):
    """Validating profile image size to be less than 5MB."""
    max_size_mb = settings.MAX_PROFILE_IMAG_SIZE_MB

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            _(f'Max file size is {max_size_mb}MB'),
            code='image_max_size'
        )

def age_validator(age):
    if age > 99:
        raise ValidationError(_(
            f'Age must be less than 99 years old...{age} is not valid.',
        ), code='age_invalid')
    elif age < 1:
        raise ValidationError(_(
            f'Age must be greater than 1 year old...{age} is not valid.'
        ), code='age_invalid')
