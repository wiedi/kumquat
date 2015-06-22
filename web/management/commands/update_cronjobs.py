from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.template.loader import render_to_string
from django.conf import settings
from cron.models import Cronjob
from subprocess import call
import uuid
import os

def update_cronjobs():
    for cronjob in Cronjob.objects.all():
        print(cronjob.when + " " + cronjob.command)

class Command(BaseCommand):
    args = ''
    help = 'generate new cronjobs and overwrite all existing'

    def handle(self, *args, **options):
        update_cronjobs()
