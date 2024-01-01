from hqm.part_reco.convolution_shape import get_shape
from .KDE_shape import get_KDE_shape
import zfit


def get_part_reco(year="2018", trigger="ETOS", preffix='', name='no_name'):
    psi2S_part_reco_shape, psi2S_ratio, _ = get_shape("psi2S_high", preffix=preffix)

    for param in psi2S_part_reco_shape.get_params():
        param.floating = False

    mass_window = (4500, 6000)

    obs = zfit.Space("B_M", limits=mass_window)

    psi2SK_shape = get_KDE_shape(obs, "psi2", "high", "psi2SK", bandwidth=None)

    psi2S_ratio *= psi2S_part_reco_shape.integrate(mass_window)[0] / psi2SK_shape.integrate(mass_window)[0]

    psi2S_ratio_param = zfit.Parameter(f"psi2S_ratio_{preffix}", psi2S_ratio)
    psi2S_ratio_param.floating = False

    total_shape = zfit.pdf.SumPDF([psi2S_part_reco_shape, psi2SK_shape], [psi2S_ratio_param], obs=obs, name=name)
    return total_shape
