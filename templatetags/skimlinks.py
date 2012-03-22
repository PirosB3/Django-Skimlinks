import urllib

from django.conf import settings
from django import template

SKIMLINK_API = "http://go.redirectingat.com/"

class SkimlinksLinkNode(template.Node):
    def __init__(self, text, link, product_id):
        self.text = text
        self.product_id = product_id
        self.link = urllib.quote_plus(link)

    def generate_link(self):
        return "".join([SKIMLINK_API, "?id=", self.product_id, "&url=",
            self.link, "&xs=1"])

    def render(self, context):
        return '<a rel="nofollow" href="%s">%s</a>' % (self.generate_link(),
                self.text)

def do_skim(parser, token):
    """returns an affiliate link"""

    # Get product ID from settings and link
    product_id = settings.SKIMLINKS_PRODUCT_ID

    # Get data from token
    contents = token.split_contents()
    if len(contents) != 3:
        raise template.TemplateSyntaxError("Syntax incorrect")
    text, link = contents[1:]

    if not product_id:
        raise template.TemplateSyntaxError("Please insert Skimlinks key")

    # Return node
    return SkimlinksLinkNode(
        text.replace('"', ''),
        link, product_id
    )

register = template.Library()
register.tag("skim", do_skim)
