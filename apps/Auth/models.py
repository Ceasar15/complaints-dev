from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

PRIMARY_REASON = (
    ('UC', 'Unprofessional Conduct'),
    ('VA', 'Verbal Abuse'),
    ('PA', 'Physical Assault'),
)

RACE_OF_OFFICER = (
    ('BL', 'Black/African'),
    ('WH', 'White/European'),
    ('AS', 'Asian'),
)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=120, blank=False)
    country = models.CharField(max_length=120, blank=False)
    state = models.CharField(max_length=120, blank=False)
    zip_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)], blank=False)
    is_official = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class EmergencyContacts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=120, blank=False)
    phone_number = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return self.user


class ComplaintsForm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    police_department = models.CharField(max_length=255)
    police_department_zip_code = models.CharField(max_length=255)
    occured_time = models.DateTimeField(auto_now=True)
    descriptions = models.TextField()
    primary_reason = models.CharField(choices=PRIMARY_REASON, max_length=255)
    race_of_officer = models.CharField(choices=RACE_OF_OFFICER, max_length=255)
    phone_number = models.CharField(max_length=255)
    upload_file = models.FileField(upload_to='complaint_upload_file', null=True, blank=True)
    were_you_arressted = models.BooleanField()


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return "Comment: {}".format(self.body)

@receiver(post_save, sender=ComplaintsForm)
def send_mail_to_user(*args, created, instance, **kwargs):
    if created:
        sender = 'ceasarkwadwo@gmail.com'
        message = 'Your complaint was created successfully.'
        subject = 'Complaint Submitted'
        recipients = [instance.user.email]
        send_mail(subject, message, sender, recipients)
        get_officials = Profile.objects.filter(zip_code=instance.user.profile.zip_code, is_official=True)
        if get_officials:
            official_recipients = [get_officials.email]
            print(33, official_recipients)
            # send_mail(subject, message, sender, official_recipients)


@receiver(post_delete, sender=User)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        print("User does not exists")
    else:
        instance.user.delete()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance,)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
