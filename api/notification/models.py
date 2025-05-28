from django.db import models
from django.utils.timezone import now
from api.common.models import BaseModel

class Notification(BaseModel):
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)

    type = models.CharField(
        max_length=50,
        choices=[("inventory", "Inventory"), ("system", "System")],
        default="system",
    )

    def __str__(self):
        return f"[{self.type.upper()}] {self.title}"