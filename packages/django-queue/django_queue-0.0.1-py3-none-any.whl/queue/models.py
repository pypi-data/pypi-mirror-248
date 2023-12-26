from django.db import models


class TaskManager(models.Manager):
    """Defines task queuing semantics."""

    def get_queryset(self, *args, **kwargs):
        """Return objects matching the base_type."""
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=self.model.base_type)

    def delay(self, *args, **kwargs):
        """Schedule for running, saving args and kwargs."""
        model = self.model(args=args, kwargs=kwargs)
        model.save()
        return model


class Task(models.Model):
    """Defines a task to be run."""
    args = models.JSONField()
    kwargs = models.JSONField()
    result = models.JSONField(null=True)

    type = models.CharField(max_length=50)
    base_type = "tasks.Task"

    objects = TaskManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
        return super().save(*args, **kwargs)

