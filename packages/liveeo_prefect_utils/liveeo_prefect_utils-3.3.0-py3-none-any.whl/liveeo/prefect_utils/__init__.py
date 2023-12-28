"""Library of utilities for Prefect (v 2.0 and later) flows that are LiveEO specific."""
import sys
from warnings import warn

if sys.version_info[1] < 10:
    # Explicitely did not use warn('...', DeprecationWarning, stacklevel=2),
    # because the deprecation warning is not for a specific line of code
    warn("LiveEO is transitioning to Python 3.10. Older Python versions will be deprecated in the near future.")
