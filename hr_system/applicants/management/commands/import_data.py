import csv
import random

from django.core.management import BaseCommand

from applicants.models import Applicant, Skill, Specialization


class Command(BaseCommand):
    """
    Импорт данных из skills.csv и applicants.csv
    Замещает все ранее созданные данные.
    Для запуска введите команду в консоль: python3 manage.py import_data
    """

    help = "Import data from skills.csv and applicants.csv files"

    def handle(self, *args, **options) -> None:
        skills_file_path = "data/skills.csv"
        applicants_file_path = "data/applicants.csv"

        self.stdout.write(
            self.style.WARNING("Removing old data from " "the database.")
        )

        Specialization.objects.all().delete()
        Skill.objects.all().delete()
        Applicant.objects.all().delete()

        self.stdout.write(self.style.WARNING("Start data import."))
        self.stdout.write(self.style.WARNING("Import specializations."))

        specializations = []

        with open(skills_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_specialization = Specialization()
                new_specialization.name = row["Направления"]
                new_specialization.position = row["Специальность"]
                specializations.append(new_specialization)
        Specialization.objects.bulk_create(specializations)

        self.stdout.write(self.style.WARNING("Import skills."))

        with open(skills_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                skill_specialization = Specialization.objects.get(
                    position=row["Специальность"]
                )

                for i in range(1, 21):
                    row_name = f"Навык {i}"
                    skill_name = row[row_name].strip()
                    if skill_name:
                        skill_instance, _ = Skill.objects.get_or_create(
                            name=skill_name
                        )
                        skill_specialization.skills.add(skill_instance)
                    else:
                        break

        self.stdout.write(self.style.WARNING("Import applicants."))

        applicants = []
        cities = [
            "Москва",
            "Санкт-Петербург",
            "Екатеринбург",
            "Сыктывкар",
            "Курган",
        ]
        country = "Россия"
        phone = "8 903 705 60 17"
        telegram = "@test_telegram"
        experience_range = 5
        activity_range = 11
        photo_path = "applicants/images/no_photo.png"
        resume_path = "applicants/resumes/test.pdf"
        resume_url = "https://www.notion.so/"
        portfolio_url = [
            "https://github.com/test_user",
            "https://www.behance.net/test_user",
        ]

        with open(applicants_file_path, "r", encoding="utf-8") as file:
            counter = 1
            reader = csv.DictReader(file)
            for row in reader:
                new_applicant = Applicant()
                first_name, last_name = row["Студент"].split()
                position = row["Специальность"]
                new_applicant.first_name = first_name
                new_applicant.last_name = last_name
                new_applicant.city = random.choice(cities)
                new_applicant.country = country
                new_applicant.email = f"test{counter}@test.com"
                counter += 1
                new_applicant.phone = phone
                new_applicant.telegram = telegram
                new_applicant.experience = random.randrange(experience_range)
                new_applicant.activity = random.randrange(activity_range)
                new_applicant.specialization = Specialization.objects.get(
                    position=position
                )
                new_applicant.photo = photo_path
                new_applicant.resume_pdf = resume_path
                new_applicant.resume_url = resume_url
                new_applicant.portfolio_url = random.choice(portfolio_url)
                new_applicant.about_me = (
                    f"Привет. Меня зовут {first_name} "
                    f"{last_name}. Я {position}."
                )

                applicants.append(new_applicant)
        Applicant.objects.bulk_create(applicants)

        for applicant in Applicant.objects.all():
            applicant.skills.set(applicant.specialization.skills.all())

        self.stdout.write(self.style.SUCCESS("Import complete."))
