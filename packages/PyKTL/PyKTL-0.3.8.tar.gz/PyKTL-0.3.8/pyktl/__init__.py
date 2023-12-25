
__version__ = "0.3.8"

__title__ = "PyKTL"
__description__ = "This library provides utility methods to generate and sign Knox Cloud Tokens using Python."
__url__ = "https://github.com/mattintech/PyKTL"
__uri__ = __url__
__doc__ = f"{__description__} <{__uri__}>"

__author__ = "Matt Hills"
__email__ = "mattintech@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright 2023 Matt Hills"

from .pyktl import generate_signed_client_identifier_jwt
from .pyktl import generate_signed_access_token_jwt

