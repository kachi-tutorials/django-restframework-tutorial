from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Event
from .serializers import EventsSerializer


@api_view(['GET'])
def events_list(request):
    data = Event.objects.all()
    context_args = {'request': request}

    serializer = EventsSerializer(data, context=context_args, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
def post_event(request):
    post_data = EventsSerializer(data=request.data, many=True)
    if post_data.is_valid():
        post_data.save()
        return Response(status=HTTP_201_CREATED)

    return Response(post_data.errors, status=HTTP_400_BAD_REQUEST)
