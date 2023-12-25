from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MockStore(TimeStampedModel):
    name = models.CharField(max_length=30)


class MockProduct(TimeStampedModel):
    name = models.CharField(max_length=30)
    store = models.ForeignKey(MockStore, on_delete=models.CASCADE)
