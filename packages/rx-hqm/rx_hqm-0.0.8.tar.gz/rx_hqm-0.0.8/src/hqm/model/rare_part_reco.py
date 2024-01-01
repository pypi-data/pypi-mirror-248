from .KDE_shape import get_KDE_shape
import zfit


def get_rare_shape(year=None, trigger=None, name='no_name', kind=None):
    mass_window = (4500, 6000)
    obs = zfit.Space("B_M", limits=mass_window)
    pdf = get_KDE_shape(obs, kind, "high", trigger=trigger, dset=year, bandwidth=None, name=name)

    return pdf 

