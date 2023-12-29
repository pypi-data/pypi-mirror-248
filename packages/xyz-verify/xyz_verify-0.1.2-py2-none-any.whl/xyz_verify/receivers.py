# -*- coding:utf-8 -*-
# author = 'denishuang'
from __future__ import unicode_literals
from django.dispatch import receiver
from .signals import to_create_verify
from . import models, choices, serializers
from django.db.models.signals import post_save
import logging
from django.contrib.contenttypes.models import ContentType

log = logging.getLogger('django')


@receiver(to_create_verify)
def create_verify(sender, **kwargs):
    target = kwargs.pop('target')
    verify = models.Verify.objects.create(
        target_type=ContentType.objects.get_for_model(target),
        target_id=target.id,
        status=choices.STATUS_PENDING,
        name=kwargs.get('name', str(target)),
        content=kwargs.get('content', {}),
        user=kwargs.get('user')
    )
    return serializers.VerifySerializer(verify).data


@receiver(post_save, sender=models.Verify)
def notify(sender, **kwargs):
    from .signals import on_notify_verify_owner
    created = kwargs['created']
    if created:
        return
    v = kwargs['instance']
    on_notify_verify_owner.send_robust(sender=type(v.owner), instance=v)
