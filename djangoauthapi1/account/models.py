from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None,otp='0'):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      print("user")
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
          otp=otp,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None,otp='0'):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      print("super")
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
          otp=otp,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  otp=models.CharField(max_length=200)
  print("02")

  objects = UserManager()
  print("14")

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


class SoldProducts(models.Model):
    product_code=models.IntegerField(primary_key=True)
    price=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    name=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    product_name=models.CharField(max_length=200)
    product_expiry=models.CharField(max_length=200)
    product_mfd=models.CharField(max_length=200)
    product_waranty=models.CharField(max_length=200)
    product_category=models.CharField(max_length=200)
    date=models.CharField(max_length=300)



