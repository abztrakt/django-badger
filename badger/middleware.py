import logging
import time
from django.conf import settings

from .models import (Badge, Award, BadgePrerequisitesNotFullfilledException)
from django.shortcuts import render_to_response
from badger import settings as bsettings
from django.template import RequestContext
import datetime


LAST_CHECK_COOKIE_NAME = getattr(settings,
    'BADGER_LAST_CHECK_COOKIE_NAME', 'badgerLastAwardCheck')


class RecentBadgeAwardsList(object):
    """Very lazy accessor for recent awards."""

    def __init__(self, request):
        self.request = request
        self.was_used = False
        self._queryset = None

        # Try to fetch and parse the timestamp of the last award check, fall
        # back to None
        try:
            self.last_check = datetime.datetime.fromtimestamp(float(
                self.request.COOKIES[LAST_CHECK_COOKIE_NAME]))
        except (KeyError, ValueError), e:
            self.last_check = None

    def process_response(self, response):
        if (self.request.user.is_authenticated() and
                (not self.last_check or self.was_used)):
            response.set_cookie(LAST_CHECK_COOKIE_NAME, time.time())
        return response

    def get_queryset(self, last_check=None):
        if not last_check:
            last_check = self.last_check

        if not (last_check and self.request.user.is_authenticated()):
            # No queryset for anonymous users or missing last check timestamp
            return None

        if not self._queryset:
            self.was_used = True
            self._queryset = (Award.objects
                .filter(user=self.request.user,
                        created__gt=last_check)
                .exclude(hidden=True))

        return self._queryset

    def __iter__(self):
        qs = self.get_queryset()
        if qs is None:
            return []
        return qs.iterator()

    def __len__(self):
        qs = self.get_queryset()
        if qs is None:
            return 0
        return len(qs)


class RecentBadgeAwardsMiddleware(object):
    """Middleware that checks for recent badge awards for the current user"""

    def process_request(self, request):
        request.recent_badge_awards = RecentBadgeAwardsList(request)
        return None

    def process_response(self, request, response):
        if not hasattr(request, 'recent_badge_awards'):
            return response
        return request.recent_badge_awards.process_response(response)


class CustomExceptionMiddleWare(object):
    def process_exception(self, request, exception):
        if isinstance(exception,BadgePrerequisitesNotFullfilledException):
            msg = msg = "The badge does not have the prerequisites completed for user " + request.user.username
            return render_to_response('%s/fail.html' %bsettings.TEMPLATE_BASE, dict(request=request, message=msg), context_instance=RequestContext(request))
