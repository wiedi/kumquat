from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings
from cron.models import Cronjob
import subprocess

def update_cronjobs():
    cronlist = ''
    cron = subprocess.Popen(settings.KUMQUAT_CRONJOB_CMD, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for cronjob in Cronjob.objects.all():
        cronlist += cronjob.when + " " + cronjob.command + "\n"

    cron.stdin.write(cronlist)
    cron.stdin.close()

class Command(BaseCommand):
    args = ''
    help = 'generate new cronjobs and overwrite all existing'

    def handle(self, *args, **options):
        update_cronjobs()
