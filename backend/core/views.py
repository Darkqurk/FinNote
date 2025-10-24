from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Stock, Holding, Trade, Price
from .serializers import StockSerializer, HoldingSerializer, TradeSerializer, PriceSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by("ticker")
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ticker"]

class HoldingViewSet(viewsets.ModelViewSet):
    serializer_class = HoldingSerializer
    filter_backends = [DjangoFilterBackend]
    def get_queryset(self):
        return HoldingSerializer.with_stats_qs()

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        total_mv = sum([h.market_value or 0 for h in qs])
        total_pnl = sum([h.pnl or 0 for h in qs])
        return Response({"total_market_value": total_mv, "total_pnl": total_pnl})

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.select_related("holding","holding__stock").all()
    serializer_class = TradeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["holding","side","date"]

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.select_related("stock").all()
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["stock","date"]

# Create your views here.
