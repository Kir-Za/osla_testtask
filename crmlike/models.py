from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class CustomerProfile(User):
    """
    Пользовательский профиль.
    """
    customer_avatar = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.username = '_'.join([self.first_name, self.last_name])
        return super().save(*args, **kwargs)


class StatusTask(models.Model):
    """
    Статус задачи. Согласно ТЗ является элементом связанного списка. В качестве указателя используется ряд целых
    чисел (index). Для реализации динамического построения списка в админке index дублируется связью ForeignKey.
    """
    title = models.CharField(max_length=200)
    index = models.FloatField(blank=True, null=False)
    insert_after = models.ForeignKey('StatusSelector', related_name='select', blank=True, null=True,
                                     on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            if self.insert_after is None:
                self.index = 0.5
            else:
                self.index = self.insert_after.previously_status + 0.5
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        ordering = ['index']


class StatusSelector(models.Model):
    """
    Модель для реальизации меню типа Select в админке.
    """
    previously_status = models.FloatField()

    def __str__(self):
        return self.select.all().first().title

    def __repr__(self):
        return str(self.previously_status)


class Task(models.Model):
    """
    Пользовательская задача.
    """
    title = models.CharField(max_length=200)
    body = models.TextField()
    time = models.DateTimeField()
    performer = models.ForeignKey('CustomerProfile', null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey('StatusTask', null=True, on_delete=models.SET_NULL)
    moderated = models.BooleanField()


@receiver(models.signals.post_save)
def check_index(sender, **kwargs):
    """
    Перехват сигнала post_save с целью сортировки поля index и обеспечения структуры связанного списка.
    """
    if sender is StatusTask and kwargs['created']:
        for tmp_selector in StatusSelector.objects.all():
            tmp_selector.delete()
        for status_num, status in enumerate(StatusTask.objects.all()):
            status.index = status_num + 1
            tmp_selector = StatusSelector(previously_status=status.index)
            tmp_selector.save()
            status.insert_after = tmp_selector
            status.save()


@receiver(models.signals.post_delete)
def remove_selector(sender, **kwargs):
    """
    Чистка объектов StatusSelector не имеющих связеей (образуются при удалении элемента в списке статусов).
    """
    if sender is StatusTask:
        removed_status = kwargs['instance']
        foreign_selecor = removed_status.insert_after
        foreign_selecor.delete()
