"""
██████╗░███████╗░██████╗░█████╗░██╗░░░██╗██████╗░
██╔══██╗██╔════╝██╔════╝██╔══██╗██║░░░██║██╔══██╗
██████╔╝█████╗░░╚█████╗░██║░░██║██║░░░██║██████╔╝
██╔══██╗██╔══╝░░░╚═══██╗██║░░██║██║░░░██║██╔═══╝░
██║░░██║███████╗██████╔╝╚█████╔╝╚██████╔╝██║░░░░░
╚═╝░░╚═╝╚══════╝╚═════╝░░╚════╝░░╚═════╝░╚═╝░░░░░

REquests + beautifulSOUP

Various convenient features related to requests.
"""

__title__ = "resoup"
__description__ = 'Various convenient features related to requests and BeautifulSoup.'
__url__ = "https://github.com/ilotoki0804/resoup"
__raw_source_url__ = "https://raw.githubusercontent.com/ilotoki0804/resoup/master"
__version_info__ = (0, 5, 2)
__version__ = str.join('.', map(str, __version_info__))
__author__ = "ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"

__github_user_name__ = __author__
__github_project_name__ = __title__

from . import requests_ as requests
from .custom_defaults import CustomDefaults
from .header_utils import clean_headers
from .sessions_with_tools import Session
from .souptools import SoupTools
from .contants import DEFAULT_HEADERS
from .broadcast_list import BroadcastList
