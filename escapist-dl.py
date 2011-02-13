# encoding: utf-8

'''a video downloader script similar in idea to the infamous youtube-dl, 
but for the escapist's video content 
(http://www.escapistmagazine.com/videos/). 
'''

import os, sys, re, json
from download import download

# some feedback options

VERBOSE = False
QUIET = False

# output/logging

def _print(*s, **kw):
    if QUIET:
        return
    newline = kw['newline'] if 'newline' in kw else True
    templine = kw['templine'] if 'templine' in kw else False
    s = ' '.join(s)
    sys.stdout.write(s.encode('unicode_escape').replace(os.path.sep.encode('unicode_escape'), os.path.sep))
    if templine and not s.endswith('\r'):
        sys.stdout.write('\r')
    if newline and not s.endswith('\n'):
        sys.stdout.write('\n')
    
def _error(s):
    print_('ERR:', s)

def _info(s):
    if VERBOSE:
        print_(s)

def main():
    # get blog url from user
    try:
        blog_url = sys.argv[1]
        if not 'escapistmagazine.com/videos/view/' in blog_url:
            reason = 'wrong url supplied'
            _error(reason)
            raise ValueError(reason)
    except:
        _print('usage: escapist-dl.py url_to_video_post')
        exit(1)

    # get & parse blog site for video config
    _info('loading `%s`' % blog_url)
    config_url = get_config_url(blog_url)
    if config_url:
        _info('found config at `%s`' % config_url)
        # get & parse video config for video info
        video_url, video_name = get_video_url_name(config_url)
        if video_url and video_name:
            _info('found clip at `%s`' % video_url)
            # get that video!
            file_name = video_name + '.mp4'
            _print('downloading `%s` ..' % file_name, newline = False)
            download(video_url, file_name)
            _print('done!')

_get_config_url_re = re.compile(r'<param name="flashvars" value="config=(?P<config_url>.*?)"/>').search
def get_config_url(blog_url):
    blog_content = download(blog_url)
    if blog_content:
        config_url = _get_config_url_re(blog_content)
        if config_url:
            return config_url.groupdict()['config_url']

def get_video_url_name(config_url):
    config_content = download(config_url)
    # fixing config to get the fucking json module to accept it
    config_content = config_content.replace("'", '"')
    config = json.loads(config_content)
    video_name = None
    try:
        video_name = config['plugins']['viral']['share']['description']
    except:
        pass
    video_url = None
    for video in config['playlist']:
        if video['url'].endswith('.mp4') and video['autoPlay'] is False: # seems ads are auto play; video content isn't
            video_url = video['url']
            break
    return video_url, video_name

if __name__ == '__main__':
    main()
