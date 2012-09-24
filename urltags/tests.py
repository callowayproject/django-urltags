from django.test import TestCase
from django.template import Context, Template


class urltagsTest(TestCase):
    """
    Tests for django-urltags
    """
    def test_add_fragment(self):
        tmpl = Template("{% load url_tags %}{{ url|add_fragment:'frgment' }}")
        ctxt = Context({'url': 'http://example.com/index.html', })
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html#frgment")

        tmpl = Template("{% load url_tags %}{{ url|add_fragment:frag }}")
        ctxt = Context({'url': 'http://example.com/index.html', 'frag': 'frgment'})
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html#frgment")

        tmpl = Template("{% load url_tags %}{{ url|add_fragment:frag }}")
        ctxt = Context({'url': 'http://example.com/index.html#old', 'frag': 'frgment'})
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html#frgment")

        tmpl = Template("{% load url_tags %}{{ url|add_fragment:frag }}")
        ctxt = Context({'url': 'http://example.com/index.html?qs=1', 'frag': 'frgment'})
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html?qs=1#frgment")

    def test_add_qs_param(self):
        tmpl = Template("{% load url_tags %}{% add_qs_param url qs 1 %}")
        ctxt = Context({'url': 'http://example.com/index.html', })
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html?qs=1")

        tmpl = Template("{% load url_tags %}{% add_qs_param url qs 1 %}")
        ctxt = Context({'url': 'http://example.com/index.html?qq=1', })
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html?qq=1&qs=1")

        tmpl = Template("{% load url_tags %}{% add_qs_param url qs 1 %}")
        ctxt = Context({'url': 'http://example.com/index.html#fragment', })
        self.assertEquals(tmpl.render(ctxt), "http://example.com/index.html?qs=1#fragment")

    def test_link(self):

        class TestObject(object):
            def get_absolute_url(self):
                return "absolute.html"

            def __unicode__(self):
                return u"TestObject"

        tmpl = Template("{% load url_tags %}{{ object|link }}")
        ctxt = Context({'object': TestObject(), })
        self.assertEquals(tmpl.render(ctxt), '<a href="absolute.html">TestObject</a>')
