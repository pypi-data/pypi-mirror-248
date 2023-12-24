# Django
from django.db import models

# 3rd Party
from model_utils.models import StatusModel
from model_utils import Choices


# Class Section
class BaseModel(models.Model):
    # Dates
    created_at = models.DateTimeField('생성일자', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True, null=True)

    class Meta:
        abstract = True


class NFT(BaseModel, StatusModel):
    STATUS = Choices(
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
    )

    # Unique
    token_id = models.IntegerField('token_id', unique=True, null=True)
    request_id = models.UUIDField('request_id', unique=True, null=True)

    # Basic
    name = models.TextField('name', blank=True, null=True)
    address = models.TextField('address', blank=True, null=True)
    nft_type = models.TextField('nft_type', blank=True, null=True)
    attributes = models.TextField('attributes', blank=True, null=True)

    # URL
    image_url = models.URLField('이미지 URL', null=True, blank=True)
    animation_url = models.URLField('영상 URL', null=True, blank=True)
    external_url = models.URLField('외부 URL', null=True, blank=True)
    extra_url = models.JSONField('추가 URL', blank=True, null=True)

    class Meta:
        verbose_name = 'nft'
        verbose_name_plural = 'nfts'
        ordering = ['-created_at']

    def clean(self):
        if self.request_id == "":
            self.request_id = None

    def save(self, *args, **kwargs):
        if self.token_id:
            self.status = 'APPROVED'
        else:
            self.status = 'PENDING'

        return super(NFT, self).save(*args, **kwargs)


class NFTHistory(BaseModel):
    nft = models.ForeignKey('creta.NFT', on_delete=models.CASCADE, related_name='histories')
    type = models.CharField('유형', max_length=100, choices=[('CREATE', 'CREATE'), ('UPDATE', 'UPDATE'), ('TRANSFER', 'TRANSFER'), ])
    title = models.TextField('제목', blank=True, null=True)

    class Meta:
        verbose_name = 'nft_history'
        verbose_name_plural = 'nft_histories'
        ordering = ['-created_at']


class ApiHistory(BaseModel):
    title = models.TextField('제목', blank=True, null=True)
    method = models.TextField('Method', blank=True, null=True)
    url = models.TextField('URL', blank=True, null=True)
    headers = models.JSONField('Header', blank=True, null=True)
    request = models.JSONField('Request', blank=True, null=True)
    response = models.JSONField('Response', blank=True, null=True)
    error = models.TextField('Error', blank=True, null=True)

    class Meta:
        verbose_name = 'history'
        verbose_name_plural = 'histories'
        ordering = ['-created_at']


