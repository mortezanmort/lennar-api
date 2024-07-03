from django.db import models
from django.urls import reverse
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import StatusModel, TimeStampedModel


class Specification(TimeStampedModel, StatusModel):
    STATUS = Choices("Planning Phase", "Planning Ready", "Design Phase", "Design Ready", "Building Phase", "Built")

    name = models.CharField(max_length=200)
    code_number = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    status = StatusField(choices=STATUS)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Specification-detail", kwargs={"pk": self.pk})


class Group(TimeStampedModel):
    name = models.CharField(max_length=50)
    group_code = models.CharField(max_length=50)
    specification = models.ForeignKey(Specification, related_name="groups", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("group-detail", kwargs={"pk": self.pk})


class Component(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    part_code = models.CharField(max_length=200, null=True, blank=True)
    specification = models.ForeignKey(Specification, related_name="components", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="components", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Component-detail", kwargs={"pk": self.pk})
