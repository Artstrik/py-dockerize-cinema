"""
Django management command to wait for the database to be available.
Place this file in: <your_app>/management/commands/wait_for_db.py
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database availability"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=60,
            help="Maximum time to wait for database (seconds)"
        )
        parser.add_argument(
            "--interval",
            type=float,
            default=1,
            help="Time between connection attempts (seconds)"
        )

    def handle(self, *args, **options):
        timeout = options["timeout"]
        interval = options["interval"]

        self.stdout.write("Waiting for database...")
        db_conn = None
        start_time = time.time()

        while not db_conn:
            try:
                # Attempt to get database connection
                db_conn = connections["default"]
                # Verify connection works
                db_conn.cursor()
            except OperationalError:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Database unavailable after {timeout} seconds"
                        )
                    )
                    raise

                self.stdout.write(
                    f"Database unavailable, waiting {interval} second(s)..."
                )
                db_conn = None
                time.sleep(interval)

        self.stdout.write(self.style.SUCCESS("Database available!"))
