from django.db import models


class Event(models.Model):
    title = models.CharField("Title", max_length=200)
    venue = models.CharField("Venue", max_length=350)
    description = models.TextField("Description")
    date = models.DateField("Date")
    adults_only = models.BooleanField("Adults_Only", default=False)
    number_of_attendees = models.IntegerField("Number_Of_Attendees")
