import urlparse
import urllib

from django.template import (Library, Node, TemplateSyntaxError, Variable,
                             VariableDoesNotExist)
from django.template.defaulttags import URLNode, url
from django.template.defaultfilters import escape
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

register = Library()


def smart_resolve(variable, context):
    """
    Return either the resolved variable or the literal value
    """
    try:
        return variable.resolve(context)
    except VariableDoesNotExist:
        return variable.var


class AddParameter(Node):
    def __init__(self, url, varname, value):
        self.url = Variable(url)
        self.varname = Variable(varname)
        self.value = Variable(value)

    def render(self, context):
        url_parts = urlparse.urlparse(smart_resolve(self.url, context))
        varname = smart_resolve(self.varname, context)
        value = smart_resolve(self.value, context)
        params = urlparse.parse_qs(url_parts.query)
        params[varname] = value
        querystring = urllib.urlencode(params, doseq=True)
        return urlparse.urlunparse(url_parts[:4] + (querystring, ) + url_parts[5:])


@register.tag
def add_qs_param(parser, token):
    """
    Called as

    {% add_qs_param url var val %}

    And adds ?var=val to the end of url, or &var=val if querystring already
    exists.
    """
    bits = token.split_contents()
    if len(bits) < 4:
        raise TemplateSyntaxError("'%s' tag requires a url, variable name and a value arguments" % bits[0])
    return AddParameter(bits[1], bits[2], bits[3])


@register.filter
def add_fragment(value, fragment):
    """
    Called as:

    {{ url|add_fragment:frag_variable }}

    or

    {{ url|add_fragment:"fragment" }}
    """
    url_parts = urlparse.urlparse(value)
    return urlparse.urlunparse(url_parts[:5] + (fragment, ))


class AbsoluteURLNode(URLNode):
    """
    From: http://djangosnippets.org/snippets/1518/
    The {% url %} templatetag is awesome sometimes it is useful to get the full
    blown URL with the domain name - for instance for links in emails. The
    {% absurl %} templatetag mirrors the behaviour of {% url %} but inserts
    absolute URLs with the domain of the current Site object.
    """
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        domain = "http://%s" % Site.objects.get_current().domain
        return urlparse.urljoin(domain, path)


@register.tag
def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but ads the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar)


@register.filter
def link(value):
    """
    From Kevin Veroneau: http://www.pythondiary.com/blog/Aug.23,2012/django-filter-be-more-dry.html

    Usage:

    {{ object|link }}
    """
    if hasattr(value, 'get_absolute_url'):
        return mark_safe('<a href="%s">%s</a>' % (escape(value.get_absolute_url()), escape(value)))
    else:
        return ''
