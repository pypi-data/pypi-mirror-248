"""HttpX + beautifulSOUP

Various convenient features related to httpx and BeautifulSoup.

██╗░░██╗██╗░░██╗░██████╗░█████╗░██╗░░░██╗██████╗░
██║░░██║╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║██╔══██╗
███████║░╚███╔╝░╚█████╗░██║░░██║██║░░░██║██████╔╝
██╔══██║░██╔██╗░░╚═══██╗██║░░██║██║░░░██║██╔═══╝░
██║░░██║██╔╝╚██╗██████╔╝╚█████╔╝╚██████╔╝██║░░░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░╚═════╝░╚═╝░░░░░
"""

__title__ = "hxsoup"
__description__ = "Various convenient features related to httpx and BeautifulSoup."
__version_info__ = (0, 2, 0)
__version__ = str.join(".", map(str, __version_info__))
__author__ = "ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"

__github_user_name__ = __author__
__github_project_name__ = __title__

from .api import delete, get, head, options, patch, post, put, request, stream
from .client import Client, AsyncClient
from .souptools import SoupedResponse, SoupTools
