from django.db import models


class SpecificationReportManager(models.Manager):
    def built_count(self):
        return (
            self.filter(status="Built")
            .values("code_number")
            .annotate(built_count=models.Count("code_number"))
            .order_by("-built_count")
        )
