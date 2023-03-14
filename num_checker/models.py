from django.db import models


class FileExtract(models.Model):
    CODE_3XX = 300
    CODE_4XX = 400
    CODE_8XX = 800
    CODE_9XX = 900

    CODE_FORMAT = (
        (CODE_3XX, '3xx'),
        (CODE_4XX, '4xx'),
        (CODE_8XX, '8xx'),
        (CODE_9XX, '9xx')
    )

    code = models.IntegerField(
        choices=CODE_FORMAT,
        verbose_name='Диапазон выписки'
    )
    file = models.FileField(
        upload_to='uploads/'
    )

    class Meta:
        ordering = ['code',]


class Registry(models.Model):
    file = models.ForeignKey(
        'FileExtract',
        on_delete=models.CASCADE,
        verbose_name='Файл с данными'
    )
    code = models.IntegerField(
        verbose_name='Код оператора'
    )
    range_from = models.BigIntegerField(
        verbose_name='Диапазон от'
    )
    range_to = models.BigIntegerField(
        verbose_name='Диапазон до'
    )
    capacity = models.IntegerField(
        verbose_name='Емкость'
    )
    operator = models.CharField(
        max_length=300,
        verbose_name='Мобильный опрератор'
    )
    region = models.CharField(
        max_length=300,
        verbose_name='Регион'
    )
    inn = models.BigIntegerField(
        verbose_name='ИНН'
    )

    class Meta:
        ordering = ['code',]
