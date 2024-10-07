import json

from django.core.management.base import BaseCommand
from pathlib import Path

from apps.common.models import Currency


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        path = Path(__file__).resolve().parent
        with open(path / 'currencies.json', 'r') as f:
            currencies_data = json.loads(f.read())

        currencies = [Currency(name=currency['name'], code=currency['code']) for currency in currencies_data]

        Currency.objects.bulk_create(currencies)

        self.stdout.write(
            self.style.SUCCESS('Currency objects successfully created')
        )
