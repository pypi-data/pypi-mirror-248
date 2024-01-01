from .__meta__ import __version__
from .context import I18nContext
from .lazy import LazyFactory, LazyProxy
from .middleware import I18nMiddleware

L = LazyFactory()

__all__ = (
    "__version__",
    "I18nContext",
    "LazyProxy",
    "I18nMiddleware",
    "L",
)
