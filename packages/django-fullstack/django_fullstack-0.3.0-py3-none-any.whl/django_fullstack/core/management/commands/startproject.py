from django_fullstack.core.management import BaseCommand
from django.core.management import execute_from_command_line
import argparse

class StartProject(BaseCommand):
    name = "startproject"
    description = "command to create new project with django"
    usage = "startapp name-project"

    def add_arguments(self, parser):
        parser.add_argument(
            "project_args",
            help="django-fullstack startproject name-project",
            nargs=argparse.REMAINDER,
        )

    def handle(self, args):
        execute_from_command_line(['django-admin'] + [args.command] + [args.project_args])
