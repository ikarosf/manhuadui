if __name__ == '__main__':
    from scrapy import cmdline

    url = '''https://www.manhuadui.com/manhua/yuyouxizhongxindeshaonvyiwenhuajiaoliudegushi/'''


    args = "scrapy crawl mhdcommon".split()
    args.append('-a')
    args.append('url='+url)
    cmdline.execute(args)