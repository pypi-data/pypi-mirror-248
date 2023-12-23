import pathlib
from urllib.parse import urlencode

from scrapy import Request
from scrapy.exceptions import CloseSpider

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.constants.domains import YANDERE_DOMAIN
from favorites_crawler.itemloaders import YanderePostItemLoader
from favorites_crawler.constants.endpoints import YANDERE_LIST_POST_URL, YANDERE_SHOW_POST_URL
from favorites_crawler.utils.files import list_yandere_id


class YandereSpider(BaseSpider):
    """Crawl voted post from yandere"""
    name = 'yandere'
    allowed_domains = (YANDERE_DOMAIN, )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = 100
        self.params = {'page': 1, 'limit': self.limit}
        self.posts = set()

    def start_requests(self):
        self.posts = set(list_yandere_id(pathlib.Path(self.settings.get('FILES_STORE')), include_subdir=True))
        self.logger.debug(f'{len(self.posts)} posts will skip download.')

        username = self.custom_settings.get('USERNAME')
        if not username:
            raise CloseSpider('Did you run "favors login yandere"?')

        self.params['tags'] = f'vote:>=1:{username}'
        yield Request(f'{YANDERE_LIST_POST_URL}?{urlencode(self.params)}')

    def parse_start_url(self, response, **kwargs):
        """Parse list post url"""
        posts = response.json()

        if len(posts) == self.limit:
            self.params['page'] += 1
            yield Request(f'{YANDERE_LIST_POST_URL}?{urlencode(self.params)}', callback=self.parse_start_url)

        for post in posts:
            if str(post['id']) in self.posts:
                continue
            loader = YanderePostItemLoader()
            loader.add_value('file_urls', post['file_url'])
            if self.settings.getbool('ENABLE_ORGANIZE_BY_ARTIST'):
                yield Request(YANDERE_SHOW_POST_URL.format(id=post['id']),
                              callback=self.parse, cb_kwargs={'loader': loader})
            else:
                yield loader.load_item()

    def parse(self, response, **kwargs):
        """Parse show post url
        @url https://yande.re/post/show/1056911
        @returns item 1
        @scrapes artist
        """
        loader = kwargs.get('loader', YanderePostItemLoader())
        loader.selector = response
        loader.add_xpath('artist', '//li[@class="tag-type-artist"]/a[last()]/text()')
        yield loader.load_item()
