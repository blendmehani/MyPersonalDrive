from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from random import randint


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, gender, email, country, city,
                    phone_number, birthdate, password=None):
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not gender:
            raise ValueError("Users must have a gender")
        if not email:
            raise ValueError("Users must have an email address")
        if not country:
            raise ValueError("Users must have a country")
        if not city:
            raise ValueError("Users must have a city or state")
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not birthdate:
            raise ValueError("Users must have their birthdate")

        user = self.model(
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            gender=gender.capitalize(),
            email=self.normalize_email(email),
            country=country.capitalize(),
            city=city.capitalize(),
            phone_number=phone_number,
            birthdate=birthdate,
        )
        user.set_password(password)
        year = birthdate.strftime('%Y')
        username = first_name.lower() + last_name.lower() + str(year)
        while User.objects.filter(username=username).exists():
            username = first_name.lower() + last_name.lower() + str(randint(1, 100000))
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, gender, email, country, city, phone_number, birthdate,
                         password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=self.normalize_email(email),
            country=country,
            city=city,
            phone_number=phone_number,
            birthdate=birthdate,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    SECRET_QUESTIONS = [
        ("1", "What was your childhood nickname?"),
        ("2", "What was the name of your second pet?"),
        ("3", "What street did you live on in third grade?")
    ]
    GENDER = [
        ('M', "Male"),
        ('F', "Female")
    ]
    first_name = models.CharField(verbose_name="First Name", max_length=20)
    last_name = models.CharField(verbose_name="Last Name", max_length=20)
    username = models.CharField(verbose_name="Username", max_length=50, unique=True)
    gender = models.CharField(verbose_name="Gender", max_length=6, choices=GENDER)
    email = models.EmailField(verbose_name="Email Address", max_length=50, unique=True)
    country = models.CharField(verbose_name="Country", max_length=20)
    city = models.CharField(verbose_name="City, State", max_length=20)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=20, unique=True)
    birthdate = models.DateField(verbose_name="Birthdate")
    secret_question = models.CharField(verbose_name="Secret Question", max_length=255, choices=SECRET_QUESTIONS)
    secret_answer = models.CharField(verbose_name="Secret Answer", max_length=20)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
#   last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True) It's created automatically by python

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'country', 'city', 'phone_number', 'birthdate']
#   avatar_picture = models.ImageField
    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True