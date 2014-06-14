from django.core.management import BaseCommand
from raw.utils import list_spiders


class Command(BaseCommand):
    help = 'List installed spiders'

    def handle(self, *args, **options):
        for spider in list_spiders():
            print spider
