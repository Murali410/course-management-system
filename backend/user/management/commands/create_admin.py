import os
from django.core.management.base import BaseCommand
from user.models import User
from organization.models import Organization, OrganizationMembership


class Command(BaseCommand):
    help = "Creates or updates the initial platform administrator and default organization"

    def handle(self, *args, **options):
        email = os.getenv("ADMIN_EMAIL", "admin@coursemanagement.com").strip()
        password = os.getenv("ADMIN_PASSWORD", "Admin@123456").strip()
        phone = os.getenv("ADMIN_PHONE", "01700000000").strip()
        first_name = os.getenv("ADMIN_FIRST_NAME", "Admin").strip()
        last_name = os.getenv("ADMIN_LAST_NAME", "User").strip()

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
                "role": "admin",
            },
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"
        user.set_password(password)
        user.save()

        # Ensure default organization exists
        org, _ = Organization.objects.get_or_create(
            slug="default",
            defaults={
                "name": "Main Coaching Center",
                "code": "MAIN01",
                "is_active": True,
            },
        )

        OrganizationMembership.objects.get_or_create(
            user=user,
            organization=org,
            defaults={
                "role": "org_admin",
                "is_default": True,
                "is_active": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Platform administrator initialized:\n"
                f"Email: {email}\n"
                f"Organization: {org.name}"
            )
        )
