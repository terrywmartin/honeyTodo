from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from django.conf import settings
from .models import Profile, User, UserSettings

#@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        is_household_admin = False
        household_user_count = User.objects.filter(household=user.household).count()
        if household_user_count == 1:
            is_household_admin = True

        profile = Profile.objects.create(
            user=user,
            household_admin = is_household_admin
        )

def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    else:
        usersettings = UserSettings.objects.create(profile=profile)
        
        
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(create_profile,sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender = Profile)

