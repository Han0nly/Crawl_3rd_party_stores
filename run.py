from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.mail import MailSender
from scrapy import settings

if __name__ == '__main__':
    mailer = MailSender.from_settings(settings)
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['']
    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
        mailer.send(to=["646861172@qq.com"], subject='%s is finished' % spider_name, body="Please check the server", cc=["lou_jd@outlook.com"])
    process.start()
