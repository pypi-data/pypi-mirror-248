import scipy_pilutil
import scipy.misc

scipy.misc.pilutil = scipy_pilutil
scipy.misc.__all__ += scipy_pilutil.__all__
for name in scipy_pilutil.__all__:
    setattr(scipy.misc, name, getattr(scipy_pilutil, name))
