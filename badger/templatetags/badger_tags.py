# django
from django import template
from django.conf import settings
from django.shortcuts import  get_object_or_404
from badger.models import Award, Badge


from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

import hashlib
import urllib

from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.filter
def permissions_for(obj, user):
    try:
        return obj.get_permissions_for(user)
    except:
        return {}


@register.filter
def key(obj, name):
    try:
        return obj[name]
    except:
        return None


@register.simple_tag
def user_avatar(user, secure=False, size=256, rating='pg', default=''):
    try:
        profile = user.get_profile()
        if profile.staff_photo:
            return profile.staff_photo.url
    except SiteProfileNotAvailable:
        pass
    except ObjectDoesNotExist:
        pass
    except AttributeError:
        pass
    return "%s/img/stock_photo.jpg" % settings.STATIC_URL 


@register.simple_tag
def badge_image(badge):
    if badge.image:
        img_url = badge.image.url
    else:
        img_url = "%s/img/default-badge.png" % settings.STATIC_URL
    return img_url

@register.simple_tag
def award_image(award):
    if award.image:
        img_url = award.image.url
    elif award.badge.image:
        img_url = award.badge.image.url
    else:
        img_url = "%s/img/default-badge.png" % settings.STATIC_URL 


        
    return img_url
    


    
@register.simple_tag
def user_award_list(badge, user):    


     if badge.allows_award_to(user):
            return '<li><a class="award_badge" href="%s">%s</a></li>' % ( reverse('badger.views.award_badge', args=[badge.slug,]), _('Issue award') )
     else:
        return ''
