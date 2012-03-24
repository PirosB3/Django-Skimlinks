import urllib

from django.conf import settings
from django import template

SKIMLINK_API = "http://go.redirectingat.com/"

class SkimlinksLinkNode(template.Node):
    def __init__(self, text, link, product_id):
        self.text = text
        self.product_id = product_id
        self.link = link

    def generate_link(self):
        return "".join([SKIMLINK_API, "?id=", self.product_id, "&url=",
            urllib.quote_plus(self.link), "&xs=1"])

    def render(self, context):
        if not self.text:
            return self.generate_link()
        return '<a rel="nofollow" href="%s">%s</a>' % (self.generate_link(),
                self.text.replace('"', ''))

def do_skim(parser, token):
    """returns an affiliate link"""

    # Get product ID from settings and raise error is PRODUCT_ID unavaliable.
    product_id = getattr(settings, "SKIMLINKS_PRODUCT_ID", None)
    if not product_id:
        raise template.TemplateSyntaxError("Product ID must be defined in settings")

    # Get data from token
    contents = token.split_contents()
    len_contents = len(contents)
    if len_contents < 2:
        raise template.TemplateSyntaxError("Syntax incorrect")

    # Assign variables from token, if text unavailable will be None.
    text = None
    if len_contents == 3:
        text, link = contents[1:]
    else:
        link = contents[1]

    # Return node.
    return SkimlinksLinkNode(
        text, link,
        product_id
    )

# Register do_skim template tag.
register = template.Library()
register.tag("skim", do_skim)
