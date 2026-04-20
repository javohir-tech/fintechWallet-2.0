# ================ DJANGO ====================
from django.db import models
from shared.models import BaseModel

class Wallet(BaseModel):
    
    class Currency(models.TextChoices):
        UZS = "UZS" , "O'zbek So'mi"
        USD = "USD" , "AQSH Dolleri"

    
    
