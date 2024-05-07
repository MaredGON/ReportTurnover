from main.models import Laboratory_Status

from django.core.management import BaseCommand

import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        states = Laboratory_Status.objects.all()
        for state in states:
            comment = state.student_comment
            if comment:
                comment = re.sub(r'\):', ' ->', comment)
                comment = comment.replace("(","")
                comment = comment.replace(")", "")
                state.student_comment = comment
                state.save()