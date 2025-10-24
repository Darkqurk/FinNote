from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=20, unique=True)   # e.g. AAPL, 005930.KS
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.ticker}"

class Holding(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="holdings")
    # 단일 사용자 과제라 user 필드 생략(MVP)

    def __str__(self):
        return f"Holding({self.stock.ticker})"

class Trade(models.Model):
    SIDE_CHOICES = [("BUY","BUY"), ("SELL","SELL")]
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name="trades")
    side = models.CharField(max_length=4, choices=SIDE_CHOICES)
    date = models.DateField()
    shares = models.DecimalField(max_digits=18, decimal_places=6)
    price = models.DecimalField(max_digits=18, decimal_places=4)  # 체결단가
    fee = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    class Meta:
        ordering = ["-date","-id"]

class Price(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField()
    close = models.DecimalField(max_digits=18, decimal_places=4)

    class Meta:
        unique_together = ("stock","date")
        ordering = ["-date"]


# Create your models here.
