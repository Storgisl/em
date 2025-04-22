from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
from .basefolder.choices import CategoryChoices, ConditionChoices, StatusChoices

User = get_user_model()

class Ad(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name="Пользователь"
    )
    title = models.CharField(
        max_length=60,
        verbose_name="Название"
    )
    description = models.TextField(
        max_length=500,
        verbose_name="Описание"
    )
    image_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="Ссылка на изображение"
    )
    category = models.CharField(
        max_length=50,
        choices=CategoryChoices.choices(),
        verbose_name="Категория"
    )
    condition = models.CharField(
        max_length=50,
        choices=ConditionChoices.choices(),
        verbose_name="Состояние"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

class ExchangeProposal(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='sent_proposals',
        verbose_name="Предлагаемый товар"
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='received_proposals',
        verbose_name="Запрашиваемый товар"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_exchanges',
        verbose_name="Отправитель",
        null=True,
        blank=True
    )
    comment = models.TextField(
        verbose_name="Комментарий"
    )
    condition = models.CharField(
        max_length=20,
        choices=StatusChoices.choices(),
        default=StatusChoices.AWAITING.value,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        unique_together = ['ad_sender', 'ad_receiver']
        ordering = ['-created_at']
