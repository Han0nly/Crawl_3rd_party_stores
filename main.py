from scrapy import cmdline

# cmdline.execute("scrapy crawl apkpurespider -s LOG_FILE=baiduspider.log".split())
# cmdline.execute("scrapy crawl baiduspider -s LOG_FILE=baiduspider.log".split())
# cmdline.execute("scrapy crawl coolapkspider -s LOG_FILE=coolapkspider.log".split())
# cmdline.execute("scrapy crawl qihuspider -s LOG_FILE=qihuspider.log".split())
# cmdline.execute("scrapy crawl qqspider -s LOG_FILE=qqspider.log".split())
# cmdline.execute("scrapy crawl wandoujiaspider -s LOG_FILE=wandoujiaspider.log".split())
# cmdline.execute("scrapy crawl xiaomispider -s LOG_FILE=xiaomispider.log".split())
# 直接运行
# cmdline.execute("scrapy crawl apkpurespider".split())
# 直接运行
# cmdline.execute("scrapy crawl baiduspider".split())
# 直接运行
# cmdline.execute("scrapy crawl coolapkspider".split())
# cmdline.execute("scrapy crawl coolapkwholespider".split())

# 直接运行
cmdline.execute("scrapy crawl qihuspider".split())
# 直接运行
# cmdline.execute("scrapy crawl qqspider".split())
# 需要限速，不然会触发阿里云验证码
# cmdline.execute("scrapy crawl wandoujiaspider".split())
# 直接运行
# cmdline.execute("scrapy crawl xiaomispider".split())
