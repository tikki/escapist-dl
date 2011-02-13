# encoding: utf-8

'''a sample script that uses escapist-dl.py to rip all(!)
zero-punctuation videos from
http://www.escapistmagazine.com/videos/view/zero-punctuation pp.
'''

import re
from download import download
edl = __import__('escapist-dl')

_allowed = re.compile('[a-zA-Z0-9 \'-()]').match
def fix_filename(filename):
    fixed = ''
    for c in filename:
        fixed += c if _allowed(c) else '_'
    return fixed

def get_video_url(blog_url):
    config_url = edl.get_config_url(blog_url)
    if config_url:
        video_url, video_name = edl.get_video_url_name(config_url)
        if video_url:
            return video_url

def main():
    # hub_url = 'http://www.escapistmagazine.com/videos/view/zero-punctuation'
    get_video_infos = re.compile('''<div class='filmstrip_video'><a href='(?P<blog_url>http://www\.escapistmagazine\.com/videos/view/zero-punctuation/.+?)'><img src='(?P<thumbnail_url>http://.+?)'></a><div class='title'>(?P<video_title>.+?)</div><div class='date'>Date: (?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{4})</div>''').findall
    
    overview_url_template = 'http://www.escapistmagazine.com/videos/view/zero-punctuation?page=%i'
    i = 1
    while 1:
        # get overview site
        print 'loading page #%i ..' % i,
        overview_url = overview_url_template % i
        i += 1
        overview = download(overview_url)
        print 'done.'
        # parse overview site
        if 'gallery_pagination_footer' not in overview:
            print 'all done! :)'
            break
        print 'loading video information ..'
        for info in get_video_infos(overview):
            blog_url, thumb_url, video_title, month, day, year = info
            print '\tdownloading `%s` ..' % video_title,
            video_url = get_video_url(blog_url)
            if not video_url:
                print 'failed!'
            else:
                file_name = '%s (%s-%s-%s).mp4' % (fix_filename(video_title), year, month, day)
                try:
                    download(video_url, file_name)
                except IOError, e:
                    print 'failed! (%s)' % e.message
                else:
                    print 'done!'
            

if __name__ == '__main__':
    main()
    