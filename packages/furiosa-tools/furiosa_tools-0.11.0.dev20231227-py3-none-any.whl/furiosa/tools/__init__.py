"""FuriosaAI tools"""

import warnings

from furiosa.common.utils import get_sdk_version

__version__ = get_sdk_version(__name__)
warnings.warn(
    "'furiosa-tools' is deprecated and will be removed in a future release.",
    category=FutureWarning,
)
