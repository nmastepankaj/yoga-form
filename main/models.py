from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
import uuid
from django.utils import timezone

# Create your models here.

def validate_age(value: int):
    """
    Validates the age value to ensure it falls within the range of 18 to 65.
    """
    if value < 18 or value > 65:
        raise ValidationError(('%(value)% should be between 18 and 56'), 
        params= {'age':value},)
    
class BaseModel(models.Model):
    """BaseModel for every children models"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Batch(models.Model):
    """
    Represents a batch in the yoga form application
    """
    batch_id=models.IntegerField(primary_key=True)
    SESSION_CHOICES = (
        ('M1', '6-7 AM'),
        ('M2', '7-8 AM'),
        ('M3', '8-9 AM'),
        ('E', '5-6 PM')
    )
    time=models.CharField(max_length=20, choices=SESSION_CHOICES)
    
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, BaseModel):
    """Account Model"""

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,null = True) 
    age=models.PositiveIntegerField(validators=[validate_age])
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=False)

    user_registered_on = models.DateTimeField(default=timezone.now, blank=True)

    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Payment(BaseModel):
    payment_id=models.CharField(max_length=264, unique=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    amount=models.PositiveIntegerField(null=False)
    date=models.DateTimeField(auto_now_add=True)
    payment_successful=models.BooleanField()

    def getnerate_payment_id(self):
        return str(self.uuid)+"-"+self.user.first_name

class Admission(BaseModel):
    admission_id=models.CharField(max_length=264, unique=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,null=False)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=False)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,null=False)

    def generate_admission_id(self):
        return str(self.uuid)+"-"+self.user.first_name