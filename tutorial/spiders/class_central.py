# -*- coding: utf-8 -*-
from scrapy import Spider, Request


class ClassCentralSpider(Spider):
    name = 'class_central'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, **kwargs):
        super().__init__(name=self.name, kwargs=kwargs)
        self.subject = kwargs.get('subject', None)

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath(
                f'//h3//*[contains(@title, "{self.subject}")]/@href'
            ).extract_first()
            yield Request(
                response.urljoin(subject_url), callback=self.parse_subject)
        else:
            self.logger.info('Scraping all subjects!')
            subjects = response.xpath(
                '//h3//*[contains(@class, "text--blue")]/@href').extract()
            for sub in subjects:
                yield Request(
                    response.urljoin(sub), callback=self.parse_subject)

    def parse_subject(self, response):
        title = response.xpath('//title/text()').extract_first()
        title = title.split('|')[0].strip()

        items = response.xpath(
            '//tr[@itemscope]//td[contains(@class, "course-name-column")]')
        for item in items:
            course_name = item.xpath(
                './/a[contains(@class, "course-name")]//span/text()'
            ).extract_first()
            course_link = item.xpath(
                './/a[contains(@class, "course-name")]/@href').extract_first()

            yield {
                'name': course_name,
                'link': response.urljoin(course_link),
            }

        next_page = response.xpath('//*[@rel="next"]/@href').extract_first()
        yield Request(response.urljoin(next_page), self.parse_subject)
