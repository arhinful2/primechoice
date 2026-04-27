from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import FileField
from django.apps import apps


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

        with transaction.atomic():
            for file_path in media_root.rglob("*"):
                if not file_path.is_file():
                    continue

                total += 1
                rel_name = file_path.relative_to(media_root).as_posix()

                if dry_run:
                    self.stdout.write(f"[DRY RUN] would upload: {rel_name}")
                    continue

                blob_url = default_storage.url(rel_name)

                if default_storage.exists(rel_name):
                    skipped += 1
                    self.stdout.write(f"[SKIP] already exists: {rel_name}")
                else:
                    with file_path.open("rb") as fh:
                        blob_url = default_storage.save(rel_name, File(fh, name=rel_name))
                    uploaded += 1
                    self.stdout.write(f"[OK] uploaded: {rel_name}")

                self._rewrite_filefield_values(rel_name, blob_url)

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run complete. {total} files scanned."))
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync complete. scanned={total}, uploaded={uploaded}, skipped={skipped}"
            )
        )

    def _rewrite_filefield_values(self, rel_name: str, blob_url: str):
        for model in apps.get_models():
            file_fields = [field for field in model._meta.get_fields() if isinstance(field, FileField)]
            if not file_fields:
                continue

            for field in file_fields:
                matches = model.objects.filter(**{f"{field.name}__in": [rel_name, f"media/{rel_name}"]})
                for instance in matches:
                    current_value = getattr(instance, field.name)
                    if getattr(current_value, "name", current_value) == blob_url:
                        continue
                    setattr(instance, field.name, blob_url)
                    instance.save(update_fields=[field.name])
