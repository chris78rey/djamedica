from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty


class Command(BaseCommand):
    help = "Carga datos semilla iniciales para desarrollo local."

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@djamedica.local",
                "first_name": "Admin",
                "last_name": "Djamedica",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        if created:
            admin_user.set_password("Admin12345!")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario admin creado: admin / Admin12345!"))

        staff_user, created = User.objects.get_or_create(
            username="recepcion",
            defaults={
                "email": "recepcion@djamedica.local",
                "first_name": "Recepción",
                "last_name": "General",
                "role": User.Role.STAFF,
                "is_staff": True,
                "is_active": True,
            },
        )
        if created:
            staff_user.set_password("Staff12345!")
            staff_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario staff creado: recepcion / Staff12345!"))

        specialty_names = [
            "Cardiología",
            "Medicina General",
            "Pediatría",
            "Traumatología",
            "Dermatología",
        ]

        specialties = {}
        for name in specialty_names:
            specialty, _ = Specialty.objects.get_or_create(
                name=name,
                defaults={"description": f"Especialidad de {name}", "is_active": True},
            )
            specialties[name] = specialty

        doctor_defs = [
            {
                "username": "dr.cardenas",
                "email": "dr.cardenas@djamedica.local",
                "first_name": "Carlos",
                "last_name": "Cárdenas",
                "license": "MED-0001",
                "specialty": "Cardiología",
            },
            {
                "username": "dra.lopez",
                "email": "dra.lopez@djamedica.local",
                "first_name": "Lucía",
                "last_name": "López",
                "license": "MED-0002",
                "specialty": "Pediatría",
            },
            {
                "username": "dr.suarez",
                "email": "dr.suarez@djamedica.local",
                "first_name": "Miguel",
                "last_name": "Suárez",
                "license": "MED-0003",
                "specialty": "Medicina General",
            },
        ]

        doctors = []
        for item in doctor_defs:
            doctor_user, created = User.objects.get_or_create(
                username=item["username"],
                defaults={
                    "email": item["email"],
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "role": User.Role.DOCTOR,
                    "is_active": True,
                },
            )
            if created:
                doctor_user.set_password("Doctor12345!")
                doctor_user.save()

            doctor_profile, _ = Doctor.objects.get_or_create(
                user=doctor_user,
                defaults={
                    "specialty": specialties[item["specialty"]],
                    "professional_license": item["license"],
                    "phone": "0990000000",
                    "office": "Consultorio 1",
                    "bio": f"Profesional de {item['specialty']}",
                    "is_available": True,
                },
            )
            doctors.append(doctor_profile)

        patient_defs = [
            ("Ana", "Pérez", "1710000001"),
            ("Luis", "Morales", "1710000002"),
            ("María", "Sánchez", "1710000003"),
            ("Jorge", "Velasco", "1710000004"),
            ("Carla", "Mena", "1710000005"),
            ("Pedro", "Almeida", "1710000006"),
            ("Sofía", "Guerrero", "1710000007"),
            ("Kevin", "Salazar", "1710000008"),
        ]

        patients = []
        for first_name, last_name, document_number in patient_defs:
            patient, _ = Patient.objects.get_or_create(
                document_number=document_number,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "document_type": Patient.DocumentType.CEDULA,
                    "phone": "0980000000",
                    "email": f"{first_name.lower()}.{last_name.lower()}@mail.local",
                    "is_active": True,
                },
            )
            patients.append(patient)

        base_dt = timezone.localtime().replace(hour=8, minute=0, second=0, microsecond=0)

        for index, patient in enumerate(patients):
            doctor = doctors[index % len(doctors)]
            scheduled_at = base_dt + timedelta(days=index // 3, hours=index % 3)

            Appointment.objects.get_or_create(
                doctor=doctor,
                scheduled_at=scheduled_at,
                defaults={
                    "patient": patient,
                    "specialty": doctor.specialty,
                    "duration_minutes": 30,
                    "status": Appointment.Status.SCHEDULED,
                    "reason": f"Consulta de control para {patient.full_name}",
                    "notes": "",
                    "created_by": staff_user,
                },
            )

        self.stdout.write(self.style.SUCCESS("Datos semilla cargados correctamente."))
