from django.test import TestCase
from django.test import Client
from .fixtures import pull_request_coment_payload
from events.models import Event
from mock import patch


class PullRequestsEventsTestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_X_GITHUB_EVENT='pull_request_review_comment')
        self.payload = pull_request_coment_payload

    @patch('events.handlers.github.github.get_issue_labels', lambda issue_number, route_config: ["test"])
    def test_comment(self):
        response = self.client.post(
            '/github_events',
            data=self.payload,
            content_type="application/json")
        self.assertEquals(response.status_code, 200)
        event = Event.objects.get(event_id="2637")  # PR number
        self.assertEquals(event.event_name, "pull_request_review_comment-created")
