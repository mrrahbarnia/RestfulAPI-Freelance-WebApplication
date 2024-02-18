import re

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
            'Password must include numbers.',
            code='password_must_include_numbers'
        )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            'Password must include letters.',
            code='password_must_include_letters'
        )

def special_character_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            'Password must include special characters.',
            code='password_must_include_special_char'
        )
