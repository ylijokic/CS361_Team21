from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField


class Musician(models.Model):
    looking_for_work = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)
    instruments = models.ManyToManyField('Instrument')
    videos = models.ManyToManyField('Video', blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    phone = models.CharField(max_length=100, blank=True)
    twitter = models.URLField(max_length=100, blank=True)
    instagram = models.URLField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Instrument(models.Model):
    name = models.CharField(max_length=100)

    class Skill(models.IntegerChoices):
        AMATEUR = 1
        INTERMEDIATE = 2
        ADVANCED = 3
        VIRTUOSO = 4

    skill_level = models.IntegerField(choices=Skill.choices)

    def save(self, *args, **kwargs):
        value = getattr(self, 'name', False)
        if value:
            setattr(self, 'name', value.title())
        super(Instrument, self).save(*args, **kwargs)

    def __str__(self):
        skill_string = {
            1: 'Amateur',
            2: 'Intermediate',
            3: 'Advanced',
            4: 'Virtuoso'
        }

        return f"{self.name} ({skill_string[self.skill_level]})"


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        value = getattr(self, 'city', False)
        if value:
            setattr(self, 'city', value.title())
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"


class Advertisement(models.Model):
    position_filled = models.BooleanField(default=False)
    creator = models.ForeignKey(Musician, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, models.PROTECT)

    def __str__(self):
        skill_string = {
            1: 'Amateur',
            2: 'Intermediate',
            3: 'Advanced',
            4: 'Virtuoso'
        }

        if not self.position_filled:
            status = 'OPEN'
        else:
            status = 'CLOSED'
        return f"[{status}] " \
               f"{self.creator.user.first_name} {self.creator.user.last_name} - " \
               f"{self.instrument.name} ({skill_string[self.instrument.skill_level]}) - " \
               f"{self.location.city}, {self.location.state}"


class Video(models.Model):
    video = EmbedVideoField()

    def __str__(self):
        return self.video
