"""
Link extraction for auto scraping
"""
from scrapy.link import Link
from scrapy.selector import XmlXPathSelector

from slybot.linkextractor.base import BaseLinkExtractor

class XmlLinkExtractor(BaseLinkExtractor):
    """Link extractor for XML sources"""
    def __init__(self, xpath, **kwargs):
        self.remove_namespaces = kwargs.pop('remove_namespaces', False)
        super(XmlLinkExtractor, self).__init__(**kwargs)
        self.xpath = xpath

    def _extract_links(self, response):
        xxs = XmlXPathSelector(response)
        if self.remove_namespaces:
            xxs.remove_namespaces()
        for url in xxs.select(self.xpath).extract():
            yield Link(url.encode(response.encoding))

class RssLinkExtractor(XmlLinkExtractor):
    """Link extraction from RSS feeds"""
    def __init__(self, **kwargs):
        super(RssLinkExtractor, self).__init__("//item/link/text()", **kwargs)

class SitemapLinkExtractor(XmlLinkExtractor):
    """Link extraction for sitemap.xml feeds"""
    def __init__(self, **kwargs):
        kwargs['remove_namespaces'] = True
        super(SitemapLinkExtractor, self).__init__("//urlset/url/loc/text() | //sitemapindex/sitemap/loc/text()", **kwargs)

class AtomLinkExtractor(XmlLinkExtractor):
     def __init__(self, **kwargs):
        kwargs['remove_namespaces'] = True
        super(AtomLinkExtractor, self).__init__("//link/@href", **kwargs)

