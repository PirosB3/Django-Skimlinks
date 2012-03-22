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
            urllib.quote_plus(link), "&xs=1"])

    def render(self, context):
        if not self.text:
            return self.generate_link()
        return '<a rel="nofollow" href="%s">%s</a>' % (self.generate_link(),
                self.text.replace('"', ''))

def do_skim(parser, token):
    """returns an affiliate link"""

    # Get product ID from settings and link
    product_id = settings.SKIMLINKS_PRODUCT_ID

    # Get data from token
    contents = list(token.split_contents())
    len_contents = len(contents)
    if len_contents < 2:
        raise template.TemplateSyntaxError("Syntax incorrect")
    if len_contents == 3:
        text, link = contents[1:]
    else:
        link = contents[1]
        text = None

    if not product_id:
        raise template.TemplateSyntaxError("Please insert Skimlinks key")

    # Return node
    return SkimlinksLinkNode(
        text,
        link, product_id
    )

register = template.Library()
register.tag("skim", do_skim)
