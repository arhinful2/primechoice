from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Upload local MEDIA_ROOT files to configured default storage (Vercel Blob)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be uploaded without uploading files.",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.exists():
            raise CommandError(f"MEDIA_ROOT does not exist: {media_root}")

        dry_run = options["dry_run"]
        total = 0
        uploaded = 0
        skipped = 0

        for file_path in media_root.rglob("*"):
            if not file_path.is_file():
                continue

            total += 1
            rel_name = file_path.relative_to(media_root).as_posix()

            if dry_run:
                self.stdout.write(f"[DRY RUN] would upload: {rel_name}")
                continue

            if default_storage.exists(rel_name):
                skipped += 1
                self.stdout.write(f"[SKIP] already exists: {rel_name}")
                continue

            with file_path.open("rb") as fh:
                default_storage.save(rel_name, File(fh, name=rel_name))
            uploaded += 1
            self.stdout.write(f"[OK] uploaded: {rel_name}")

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run complete. {total} files scanned."))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. scanned={total}, uploaded={uploaded}, skipped={skipped}"
            )
        )
