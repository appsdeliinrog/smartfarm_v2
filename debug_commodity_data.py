"""Check commodities and price data"""
import os
import sys
import django

# Setup Django
sys.path.append(r'c:\Users\fsociety\Documents\agri-open')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import PriceObservation, Commodity
from django.db.models import Count

print("=== COMMODITY AND PRICE DATA DEBUG ===")
print(f"Total price observations: {PriceObservation.objects.count()}")
print(f"Total commodities: {Commodity.objects.count()}")

print("\n📊 Commodities with price data:")
for item in PriceObservation.objects.values('commodity__name').annotate(count=Count('id')).order_by('commodity__name'):
    print(f"- {item['commodity__name']}: {item['count']} observations")

print("\n🏪 Latest prices by commodity:")
# Get latest price for each commodity (SQLite compatible)
for commodity in Commodity.objects.all():
    latest_price = PriceObservation.objects.filter(commodity=commodity).order_by('-observed_date').first()
    if latest_price:
        print(f"- {commodity.name}: {latest_price.price} TZS/kg on {latest_price.observed_date} at {latest_price.market.name}")

print("\n🔍 Date range of price data:")
from django.db.models import Min, Max
date_range = PriceObservation.objects.aggregate(
    earliest=Min('observed_date'),
    latest=Max('observed_date')
)
print(f"From {date_range['earliest']} to {date_range['latest']}")

# Check for recent price data (last 30 days)
from datetime import datetime, timedelta
recent_cutoff = datetime.now().date() - timedelta(days=30)
recent_count = PriceObservation.objects.filter(observed_date__gte=recent_cutoff).count()
print(f"\n📅 Recent price observations (last 30 days): {recent_count}")

if recent_count == 0:
    print("⚠️  WARNING: No recent price data found! This might explain filtering issues.")
    # Show the most recent price observations
    print("\n🕒 Most recent price observations:")
    recent_prices = PriceObservation.objects.order_by('-observed_date')[:10]
    for price in recent_prices:
        print(f"- {price.commodity.name}: {price.observed_date} ({price.market.name})")
