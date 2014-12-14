from django.core.management import BaseCommand
import csv
from chb.models import ChbStop, ChbQuay
from utils.geo import rd_wgs84

__author__ = 'joelthuis'

class Command(BaseCommand):
    args = '<folder>'
    help = 'Import central stop db'

    stopplace_cache = {}

    def handle(self, *args, **options):
        self.import_stopplaces(args[0])
        self.import_quays(args[0])

    def import_stopplaces(self, folder):
        ChbStop.objects.all().delete()
        with open(folder+'opendrgl_stopplace.csv', 'rb') as csvfile:
            stopplace = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in stopplace:
                stop = ChbStop()
                stop.public_code = row['stopplacecode']
                stop.name = row['publicname']
                stop.city = row['town']
                stop.type = row['stopplacetype']
                stop.save()
                self.stopplace_cache[stop.public_code] = stop.pk
                i += 1
                if i % 100 == 0:
                    print "Did %s stopplaces" % i

    def import_quays(self, folder):
        ChbQuay.objects.all().delete()
        with open(folder+'opendrgl_quay.csv', 'rb') as csvfile:
            quay = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in quay:
                quay = ChbQuay()
                quay.stop_id = self.stopplace_cache[row['stopplacecode']]
                quay.public_code = row['quaycode']
                coords = rd_wgs84(float(row['rd_x']), float(row['rd_y']))
                quay.lat = coords[0]
                quay.lng = coords[1]
                quay.name = row['quayname']
                quay.city = row['town']
                quay.save()
                i += 1
                if i % 100 == 0:
                    print "Did %s quays" % i
