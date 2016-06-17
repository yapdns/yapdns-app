from __future__ import unicode_literals

import binascii
import os
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


def generate_secret_key():
    return binascii.hexlify(os.urandom(24))


@python_2_unicode_compatible
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    secret_key = models.CharField(max_length=48, default=generate_secret_key, editable=False)

    def __str__(self):
        return '%s' % (self.name)
