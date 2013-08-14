# -*- coding:utf-8 -*-
from django.conf import settings
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    is_collab = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


#
# Falta agregar el comportamiento para la creación del perfil cuando se cree un usuario nuevo.
#
