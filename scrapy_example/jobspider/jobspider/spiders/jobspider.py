import scrapy


class JobSpider(scrapy.Spider):
    name = "jobspider"
    start_urls = ['https://www.indeed.com/jobs?q=web+scraping']
    job_counter = 0
    base_url = 'https://www.indeed.com'

    def parse(self, response):
        for job in response.css('div.title'):
            self.job_counter += 1
            job_title = job.css("a ::text").extract_first().replace("\n", "").strip()
            job_link = job.css("a ::attr(href)").extract_first()
            yield {self.job_counter: {'title': job_title, 'link': self.base_url + job_link}}

        pagination = response.css('.pagination > a::attr(href)').extract()
        for next_page in pagination:
            yield response.follow(self.base_url + next_page, self.parse)
