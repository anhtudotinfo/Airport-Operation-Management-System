from ctypes.wintypes import RGB
from statistics import quantiles
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model

from io import BytesIO
from PIL import Image
from django.core.files import File

# Create your models here.

# User Manager model
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('a_passenger', False)
        extra_fields.setdefault('an_airport_admin', False)
        extra_fields.setdefault('an_airline_admin', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password, first_name, last_name, **extra_fields)
        return user


# User model
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, primary_key=True)
    # password, first_name, last_name, already part of AbstractUser
    a_passenger = models.BooleanField(default=False, help_text='Determines whether the user is a passenger', verbose_name='passenger status')
    an_airport_admin = models.BooleanField(default=False, help_text='Determines whether the user is an airport admin', verbose_name='airport admin status')    
    an_airline_admin = models.BooleanField(default=False, help_text='Determines whether the user is an airline admin', verbose_name='airline admin status')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # email, password, automatically required

    # user properties
    @property
    def is_passenger(self):
        return self.passenger

    @property
    def is_airport_admin(self):
        return self.airport_admin

    @property
    def is_airline_admin(self):
        return self.airline_admin

    objects = UserManager()


user = get_user_model()


# Passenger model
class Passenger(models.Model):
    email = models.OneToOneField(user, on_delete=models.CASCADE, related_name='passenger')
    ssn = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = 'passenger'

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return f'/{self.email}/'


# Airport Admin model
class AirportAdmin(models.Model):
    email = models.OneToOneField(user, on_delete=models.CASCADE, related_name='airport_admin')
    admin_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'airport_admin'

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return f'/{self.email}/'


# Airline Admin model
class AirlineAdmin(models.Model):
    email = models.OneToOneField(user, on_delete=models.CASCADE, related_name='airline_admin')
    employee_id = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = 'airline_admin'

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return f'/{self.email}/'


# Company model
class Company(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    admin = models.ForeignKey(AirportAdmin, on_delete=models.SET_NULL, null=True, related_name='companies')

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'


# Hotel model
class Hotel(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='hotels')
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='hotel_images/', blank=True, null=True)

    class Meta:
        db_table = 'hotel'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.id}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


# Transaction model
class Transaction(models.Model):
    transac_id = models.PositiveIntegerField(primary_key=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='transactions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'transaction'

    def __str__(self):
        return f'transaction {self.transac_id} by {self.passenger}'

    def get_absolute_url(self):
        return f'/{self.transac_id}/'


# Stay model
class Stay(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='stays')
    transac = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='stays')
    image = models.ImageField(upload_to='stay_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='stay_images/', blank=True, null=True)

    class Meta:
        db_table = 'stay'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.hotel.id}/{self.id}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


# Airport Complaint model
class AirportComplaint(models.Model):
    complaint_id = models.PositiveIntegerField(primary_key=True)
    description = models.TextField()
    admin = models.ForeignKey(AirportAdmin, on_delete=models.SET_NULL, null=True, related_name='airport_complaints')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='airport_complaints')

    class Meta:
        db_table = 'airport_complaint'

    def __str__(self):
        return f'complaint {self.complaint_id} by {self.passenger}, resolved by {self.admin}'

    def get_absolute_url(self):
        return f'/{self.complaint_id}/'


# Airline model
class Airline(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    location = models.CharField(max_length=255)

    class Meta:
        db_table = 'airline'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'


# Airline Complaint model
class AirlineComplaint(models.Model):
    complaint_id = models.PositiveIntegerField(primary_key=True)
    description = models.TextField()
    admin = models.ForeignKey(AirlineAdmin, on_delete=models.SET_NULL, null=True, related_name='airline_complaints')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='airline_complaints')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airline_complaints')

    class Meta:
        db_table = 'airline_complaint'

    def __str__(self):
        return f'complaint {self.complaint_id} by {self.passenger}, resolved by {self.admin}'

    def get_absolute_url(self):
        return f'/{self.complaint_id}/'


# Airplane model
class Airplane(models.Model):
    pid = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    economy_seats = models.PositiveIntegerField()
    premium_economy_seats = models.PositiveIntegerField()
    business_seats = models.PositiveIntegerField()
    first_seats = models.PositiveIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')

    class Meta:
        db_table = 'airplane'

    def __str__(self):
        return f'{self.airline} - {self.pid}'

    def get_absolute_url(self):
        return f'/{self.pid}/'


# Destination model
class Destination(models.Model):
    airport_code = models.CharField(max_length=3, primary_key=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        db_table = 'destination'

    def __str__(self):
        return self.airport_code

    def get_absolute_url(self):
        return f'/{self.airport_code}/'


# Flight model
class Flight(models.Model):
    flight_num = models.PositiveIntegerField(primary_key=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    dep_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    dest = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, related_name='flights')
    plane = models.ForeignKey(Airplane, on_delete=models.SET_NULL, null=True, related_name='flights')

    class Meta:
        db_table = 'flight'

    def __str__(self):
        return f'{self.airline} - {self.flight_num}'

    def get_absolute_url(self):
        return f'/{self.flight_num}/'


# Fare model
class Fare(models.Model):
    fare_id = models.PositiveIntegerField(primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cabin = models.CharField(max_length=255)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='fares')
    tickets = models.PositiveIntegerField()

    class Meta:
        db_table = 'fare'

    def __str__(self):
        return f'{self.flight} - {self.fare_id}'

    def get_absolute_url(self):
        return f'/{self.flight}/{self.fare_id}/'


# Ticket model
class Ticket(models.Model):
    ticket_id = models.PositiveIntegerField(primary_key=True)
    seat_pos = models.CharField(max_length=255)
    passenger = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True, related_name='tickets')
    fare = models.ForeignKey(Fare, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        db_table = 'ticket'

    def __str__(self):
        return f'{self.ticket_id}'

    def get_absolute_url(self):
        return f'/{self.fare}/{self.ticket_id}/'

