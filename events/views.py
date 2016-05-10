from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .handlers.github import GithubRequestEventHandler
from .handlers.jenkins import JenkinsRequestEventHandler
from .models import Event


class HookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HookView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        event = GithubRequestEventHandler(request)
        event.parse()
        if event.should_alert():
            Event.objects.create(
                event_data=event.payload,
                event_name=event.event_name,
                event_id=event.event_id
            )
        return HttpResponse("OK")


class JenkinsPRView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JenkinsPRView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        event = JenkinsRequestEventHandler()
        event.parse(request)
        return HttpResponse("OK")
