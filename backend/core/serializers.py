from rest_framework import serializers
from .models import Stock, Holding, Trade, Price
from django.db.models import Sum, F, DecimalField, Case, When

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id","ticker","name"]

class PriceSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        source="stock", queryset=Stock.objects.all(), write_only=True
    )
    class Meta:
        model = Price
        fields = ["id","stock","stock_id","date","close"]

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id","holding","side","date","shares","price","fee"]

class HoldingSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        source="stock", queryset=Stock.objects.all(), write_only=True
    )
    quantity = serializers.DecimalField(max_digits=18, decimal_places=6, read_only=True)
    avg_cost = serializers.DecimalField(max_digits=18, decimal_places=6, read_only=True)
    last_close = serializers.DecimalField(max_digits=18, decimal_places=4, read_only=True)
    market_value = serializers.DecimalField(max_digits=18, decimal_places=4, read_only=True)
    pnl = serializers.DecimalField(max_digits=18, decimal_places=4, read_only=True)

    class Meta:
        model = Holding
        fields = ["id","stock","stock_id","quantity","avg_cost","last_close","market_value","pnl"]

    @staticmethod
    def with_stats_qs():
        # 수량 = BUY - SELL
        qty_buy = Sum(Case(When(trades__side="BUY", then=F("trades__shares")), default=0, output_field=DecimalField(max_digits=18, decimal_places=6)))
        qty_sell = Sum(Case(When(trades__side="SELL", then=F("trades__shares")), default=0, output_field=DecimalField(max_digits=18, decimal_places=6)))
        qty = qty_buy - qty_sell
        # 원가총액 = ∑(BUY shares*price + fee) - ∑(SELL에 대한 원가차감은 단순화: 제외)
        gross_buy = Sum(Case(When(trades__side="BUY", then=F("trades__shares")*F("trades__price")+F("trades__fee")), default=0, output_field=DecimalField(max_digits=18, decimal_places=6)))
        avg_cost = Case(When(**{"trades__isnull": False, "then": gross_buy / Case(When(then=qty, condition=~(qty==0)), default=1) }), default=0, output_field=DecimalField(max_digits=18, decimal_places=6))
        # 최근 종가
        from django.db.models import Subquery, OuterRef
        from .models import Price
        latest_price = Price.objects.filter(stock=OuterRef("stock")).order_by("-date").values("close")[:1]
        return Holding.objects.all().annotate(
            quantity=qty,
            avg_cost=avg_cost,
            last_close=Subquery(latest_price, output_field=DecimalField(max_digits=18, decimal_places=4)),
            market_value=Case(When(~(qty==0), then=qty*Subquery(latest_price)), default=0, output_field=DecimalField(max_digits=18, decimal_places=4)),
            pnl=Case(When(~(qty==0), then=qty*(Subquery(latest_price)-avg_cost)), default=0, output_field=DecimalField(max_digits=18, decimal_places=4)),
        )
