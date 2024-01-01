import os
import hist
import zfit
import numpy
import zutils.utils as zut
import utils_noroot as utnr

from importlib.resources import files
from zutils.pdf          import SUJohnson
from hqm.tools.utility   import load_pickle
from hqm.tools.utility   import get_project_root
from hqm.tools.utility   import read_root
from hqm.tools.Cut       import Cut
from logzero             import logger

#--------------------------------------------
class CacheCmbShape:
    _all_cmb_shapes = {}

    @classmethod
    def __call__(cls, q2, pdf=None):
        if pdf is None:
            if q2 in cls._all_cmb_shapes:
                return cls._all_cmb_shapes[q2]
            else:
                return None
        else:
            cls._all_cmb_shapes[q2] = pdf
#--------------------------------------------
class data:
    cmb_normalisation_region = 5500, 6000
    mass_window              = 4000, 6000
    split_point              = 5180
#--------------------------------------------
def get_correction_DSCB(obs, suffix):
    mu = zfit.Parameter(f"correction_DSCB_mu_{suffix}", 0, -100, 100)
    sigma = zfit.Parameter(f"correction_DSCB_sigma_{suffix}", 40, 0.1, 100)
    al = zfit.Parameter(f"correction_DSCB_al_{suffix}", 1.5, 0.001, 10)
    nl = zfit.Parameter(f"correction_DSCB_nl_{suffix}", 1, 0.001, 110)
    ar = zfit.Parameter(f"correction_DSCB_ar_{suffix}", 1.5, 0.001, 10)
    nr = zfit.Parameter(f"correction_DSCB_nr_{suffix}", 1, 0.001, 110)

    correction_DSCB = zfit.pdf.DoubleCB(
        obs=obs, mu=mu, sigma=sigma, alphal=al, nl=nl, alphar=ar, nr=nr, name="correction_DSCB"
    )
    return correction_DSCB
#--------------------------------------------
def get_correction_left_CB(obs, suffix):
    mu = zfit.Parameter(f"correction_left_CB_mu_{suffix}", -100, -500, 0)
    sigma = zfit.Parameter(f"correction_left_CB_sigma_{suffix}", 5, 0.001, 100)
    alpha = zfit.Parameter(f"correction_left_CB_alpha_{suffix}", 0.5, 0.001, 2)
    n = zfit.Parameter(f"correction_left_CB_n_{suffix}", 50, 1, 110)

    correction_left_CB = zfit.pdf.CrystalBall(obs=obs, mu=mu, sigma=sigma, alpha=alpha, n=n, name="correction_left_CB")
    return correction_left_CB
#--------------------------------------------
def get_correction_right_CB(obs, suffix):
    mu = zfit.Parameter(f"correction_right_CB_mu_{suffix}", 100, 0, 500)
    sigma = zfit.Parameter(f"correction_right_CB_sigma_{suffix}", 5, 0.001, 100)
    alpha = zfit.Parameter(f"correction_right_CB_alpha_{suffix}", -0.5, -2, -0.001)
    n = zfit.Parameter(f"correction_right_CB_n_{suffix}", 50, 1, 110)

    correction_right_CB = zfit.pdf.CrystalBall(
        obs=obs, mu=mu, sigma=sigma, alpha=alpha, n=n, name="correction_right_CB"
    )
    return correction_right_CB
#--------------------------------------------
def set_values(s_par, d_par, preffix):
    for par in s_par:
        name = par.name.replace(f'_{preffix}', '')
        try:
            val, err = d_par[name]
        except:
            logger.error(f'Cannot access {name}, found:')
            for key in d_par:
                logger.info(key)
            raise

        par.set_value(val)
#--------------------------------------------
def load_pdf(pickle_path, pdf, preffix):
    name      = pickle_path.replace('/', '_').replace('.', '_p_')
    json_path = files('hqm_data').joinpath(f'pars/{name}.json')
    if not os.path.isfile(json_path):
        obj    = load_pickle(pickle_path)
        res    = obj["result"]
        d_par  = zut.res_to_dict(res, frozen=True)
        utnr.dump_json(d_par, json_path)
    else:
        logger.debug(f'Loading parameters from: {json_path}')
        d_par  = utnr.load_json(json_path)

    s_par = pdf.get_params()
    set_values(s_par, d_par, preffix)

    return pdf
#--------------------------------------------
def get_data(root_path, trigger):
    BDT_cmb      = Cut(lambda x: x.BDT_cmb > 0.831497)
    BDT_prc      = Cut(lambda x: x.BDT_prc > 0.480751)
    BDT          = BDT_cmb & BDT_prc
    data_array   = read_root(root_path, trigger)
    data_array   = BDT.apply(data_array)

    return data_array
#--------------------------------------------
def get_cuts():
    cmb_normalisation_region_cut = Cut(lambda x: (x.B_M > data.cmb_normalisation_region[0]) & (x.B_M < data.cmb_normalisation_region[1]) )
    mass_window_cut              = Cut(lambda x: (x.B_M > data.mass_window[0])              & (x.B_M < data.mass_window[1]))
    split_point_cut              = Cut(lambda x:  x.B_M < data.split_point)

    part_reco_cut                = mass_window_cut &  split_point_cut
    sig_cut                      = mass_window_cut & ~split_point_cut

    return sig_cut, part_reco_cut, cmb_normalisation_region_cut
#--------------------------------------------
def get_yields(data_array, cmb_shape):
    sig_cut, part_reco_cut, cmb_normalisation_region_cut = get_cuts()

    cmb_total_yield = ( cmb_normalisation_region_cut.get_entries(data_array) / cmb_shape.integrate(data.cmb_normalisation_region, norm=data.mass_window)[0] )
    part_reco_yield = ( part_reco_cut.get_entries(data_array) - cmb_total_yield * cmb_shape.integrate((data.mass_window[0], data.split_point), norm=data.mass_window)[0] )
    sig_yield       = ( sig_cut.get_entries(data_array)       - cmb_total_yield * cmb_shape.integrate((data.split_point, data.mass_window[1]), norm=data.mass_window)[0] )

    return [sig_yield.numpy(), part_reco_yield.numpy(), cmb_total_yield.numpy()]
#--------------------------------------------
def get_hist(l_mas, cmb_shape, cmb_total_yield):
    part_reco_region_hist = hist.Hist.new.Regular( 100, data.mass_window[0], data.split_point, overflow=False, name='B_M').Double()
    part_reco_region_hist.fill(l_mas)

    binning               = zfit.binned.RegularBinning(100, data.mass_window[0], data.split_point, name="B_M")
    binned_obs            = zfit.Space("B_M", binning=binning)
    binned_pdf            = cmb_shape.to_binned(binned_obs)
    cmb_hist              = binned_pdf.to_hist()
    cmb_hist              = (
        cmb_hist
        / cmb_hist.sum().value
        * zfit.run(cmb_total_yield * cmb_shape.integrate((data.mass_window[0], data.split_point), norm=data.mass_window)[0])
    )

    logger.info(f'cmb_hist.sum(): {cmb_hist.sum().value}')

    part_reco_hist = part_reco_region_hist - cmb_hist

    return part_reco_hist
#--------------------------------------------
def get_cmb_mm_shape(q2, obs, preffix=''):
    cached_shape = CacheCmbShape()
    comb_mm = cached_shape(q2)
    if comb_mm is None:
        mu_cmb = zfit.Parameter(f"cmb_mm_mu_{q2}_{preffix}", 4000, 3500, 5000)
        scale_cmb = zfit.Parameter(f"cmb_mm_scale_{q2}_{preffix}", 10, 0.1, 100)
        a = zfit.Parameter(f"cmb_mm_a_{q2}_{preffix}", -10, -20, 0)
        b = zfit.Parameter(f"cmb_mm_b_{q2}_{preffix}", 1, 0, 10)
        comb_mm = SUJohnson(obs=obs, mu=mu_cmb, lm=scale_cmb, gamma=a, delta=b, name=f"comb_mm_{q2}_{preffix}")
        pickle_path = (
            get_project_root() + f"data/comb_mm/latest/{q2}_2018_B_M_NoBDTprc/{q2}_2018_B_M_NoBDTprc_fit_result.pickle"
        )
        comb_mm = load_pdf(pickle_path, comb_mm, preffix)
        cached_shape(q2, comb_mm)
    return comb_mm
#--------------------------------------------
def get_inputs(cmb_shape):
    project_root = get_project_root()
    root_path    = f'{project_root}/root_sample/v5/data/v10.21p2/2018_MTOS/psi2_nomass.root'
    json_name    = root_path.replace('/', '_').replace('.', '_p_') + '_prc_shape.json'
    json_path    = files('hqm_data').joinpath(f'pars/{json_name}')

    if os.path.isfile(json_path):
        logger.info(f'Found cached data: {json_path}')
        d_data        = utnr.load_json(json_path)
        l_yld         = d_data['yields']
        l_mas         = d_data['bmass']
    else:
        logger.info(f'Not found cached data: {json_path}')
        mm_data       = get_data(root_path, 'MTOS')
        l_yld         = get_yields(mm_data, cmb_shape)
        part_reco_cut = get_cuts()[1]
        mm_data       = part_reco_cut.apply(mm_data)
        l_mas         = mm_data.B_M.tolist()

        utnr.dump_json({'yields' : l_yld, 'bmass' : l_mas}, json_path)

    return l_yld, l_mas
#--------------------------------------------
def get_shape(kind, preffix='', plot_cmb=None):
    if   kind != "psi2S_high":
        logger.error(f'Kind {kind} not implemented')
        raise

    obs                         = zfit.Space("B_M", limits=(4000, 6000))
    cmb_shape                   = get_cmb_mm_shape(q2="psi2", obs=obs, preffix=preffix)
    l_yld, l_mas                = get_inputs(cmb_shape)
    [sig_yld, prc_yld, cmb_yld] = l_yld

    obs_kernel           = zfit.Space("B_M", limits=(-800, 1200))
    correction_function  = get_correction_right_CB(obs_kernel, suffix=f'{kind}_{preffix}')
    project_root         = get_project_root()
    pickle_path          = f'{project_root}/data/part_reco/fit_convolution/latest/{kind}/fit_result.pickle'
    correction_function  = load_pdf(pickle_path, correction_function, preffix)

    part_reco_hist       = get_hist(l_mas, cmb_shape, cmb_yld) 
    part_reco_pdf        = zfit.pdf.HistogramPDF(part_reco_hist)
    part_reco_unbinned   = zfit.pdf.UnbinnedFromBinnedPDF(part_reco_pdf, zfit.Space("B_M", limits=(3000, 7000)))
    convolution_shape    = zfit.pdf.FFTConvPDFV1(
        func  = part_reco_unbinned,
        kernel= correction_function,
        name  = f'convolution_shape_{kind}',
        n     = 1000
    )

    return convolution_shape, prc_yld/sig_yld, part_reco_hist
#--------------------------------------------
