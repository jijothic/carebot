import copytext
from dateutil.parser import parse
import logging
import requests
from util.s3 import Uploader

import app_config

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = Uploader()

class Screnshotter:
    """
    Given a story URL, get a screenshot
    """
    def get_story_image(self, story_url):
        url = "http://carebot-capture.herokuapp.com/api/image?id=%s&url=%s" % ('storytext', story_url)
        r = requests.get(url)

        if r.status_code == 200:
          url = s3.upload(r.content, dir='screenshots')
          return url

        logger.info("Error % getting screenshot via %s" % (r.status_code, url))
        return None


