import urllib

from django.conf import settings
from django import template

SKIMLINK_API = "http://go.redirectingat.com/"

class SkimlinksLinkNode(template.Node):
    def __init__(self, link, product_id):
        self.link = urllib.quote_plus(link)
        self.product_id = product_id

    def render(self, context):
        return "".join([SKIMLINK_API, "?id=", self.product_id, "&url=",
            self.link, "&xs=1"])

def do_skim(parser, token):
    """returns an affiliate link"""

    # Get product ID from settings and link
    product_id = settings.SKIMLINKS_PRODUCT_ID
    link = token.split_contents()[1]
    if not product_id:
        raise template.TemplateSyntaxError("Please insert Skimlinks key")
    return SkimlinksLinkNode(link, product_id)

register = template.Library()
register.tag("skim", do_skim)
