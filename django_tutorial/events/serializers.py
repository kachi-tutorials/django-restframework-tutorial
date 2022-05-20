from rest_framework.serializers import ModelSerializer
from .models import Event


class EventsSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "venue",
            "description",
            "date",
            "number_of_attendees"
        ]