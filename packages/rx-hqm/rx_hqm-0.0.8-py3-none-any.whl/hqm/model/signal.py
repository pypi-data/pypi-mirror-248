from importlib.resources import files
from hqm.tools.utility   import get_project_root
from hqm.tools.utility   import load_pickle
from hqm.tools.utility   import read_root
from hqm.tools.Cut       import Cut
from monitor.ms_reader   import ms_reader

from logzero import logger

import os
import zfit
import zutils.utils as zut
import utils_noroot as utnr

class CacheMSReader:
    scales = {"mu": None, "sg": None, "br": None}
    rdr = None

    def __init__(self):
        previous_caldir = ""
        try:
            previous_caldir = os.environ["CASDIR"]
        except KeyError:
            pass

        os.environ["CASDIR"] = "/publicfs/lhcb/user/campoverde/Data/cache"

        if CacheMSReader.rdr is None:
            CacheMSReader.rdr = ms_reader(version="v4")

        for scale, value in CacheMSReader.scales.items():
            if value is None:
                CacheMSReader.scales[scale] = CacheMSReader.rdr.get_scales(scale, avg_dset=True)

        os.environ["CASDIR"] = previous_caldir

    def get_scale(self, scale):
        return CacheMSReader.scales[scale]

def set_values(s_par, d_par, preffix):
    for par in s_par:
        name = par.name.replace(f'_{preffix}', '')
        if name.startswith('dmu_') or name.startswith('ssg_'):
            continue

        try:
            val, _ = d_par[name]
        except:
            logger.error(f'Cannot access {name}, found:')
            for key in d_par:
                logger.info(key)
            raise

        par.set_value(val)

def load_pdf(pickle_path, pdf, preffix):
    pickle_name = pickle_path.replace('/', '_').replace('.', '_p_')
    json_path   = files('hqm_data').joinpath(f'pars/{pickle_name}.json')
    if not os.path.isfile(json_path):
        obj     = load_pickle(pickle_path)
        res     = obj["result"]
        d_par   = zut.res_to_dict(res, frozen=True)
        utnr.dump_json(d_par, json_path)
    else:
        logger.debug(f'Loading PDF parameters from: {json_path}')
        d_par=utnr.load_json(json_path)

    params = pdf.get_params()
    set_values(params, d_par, preffix)

    return pdf

def load_signal_ee_brem(preffix, brem_category, obs, year, trigger, dmu, ssg):
    mu = zfit.Parameter(f"mu_DSCB_{brem_category}_{preffix}", 5200, 5000, 5600)
    _mu = zfit.param.ComposedParameter(
        f"_mu_DSCB_ee_{brem_category}_{preffix}", lambda p: p["mu"] + p["dmu"], params={"mu": mu, "dmu": dmu}
    )
    sigma = zfit.Parameter(f"sigma_DSCB_{brem_category}_{preffix}", 10, 0.1, 500)
    _sigma = zfit.param.ComposedParameter(
        f"_sigma_DSCB_ee_{brem_category}_{preffix}", lambda p: p["sigma"] * p["ssg"], params={"sigma": sigma, "ssg": ssg}
    )
    alphal = zfit.Parameter(f"alphal_DSCB_{brem_category}_{preffix}", 1, 0, 20)
    nl = zfit.Parameter(f"nl_DSCB_{brem_category}_{preffix}", 1, 0, 150)
    alphar = zfit.Parameter(f"alphar_DSCB_{brem_category}_{preffix}", 1, 0, 20)
    nr = zfit.Parameter(f"nr_DSCB_{brem_category}_{preffix}", 1, 0, 120)

    dscb = zfit.pdf.DoubleCB(
        mu=_mu,
        sigma=_sigma,
        alphal=alphal,
        nl=nl,
        alphar=alphar,
        nr=nr,
        obs=obs,
        name=f"DSCB_{brem_category}_{preffix}",
    )
    pickle_path = (
        get_project_root() + f"data/signal_shape_ee/latest/fit_Bu2Kee_MC_2018_ETOS_high_normal_{brem_category}.pickle"
    )
    dscb = load_pdf(pickle_path, dscb, preffix)
    for param in [mu, sigma, alphal, nl, alphar, nr]:
        param.floating = False

    return dscb

def get_br_frac():
    sign_MC_path = get_project_root() + "root_sample/v5/sign/v10.21p2/2018_ETOS/high_normal.root"
    json_path    = sign_MC_path.replace('/', '_').replace('.', '_p_')
    json_path    = files('hqm_data').joinpath(f'{json_path}_br_frac.json')
    if os.path.isfile(json_path):
        [f0, f1, f2] = utnr.load_json(json_path)
        return f0, f1, f2

    bdt_cmb = Cut(lambda x: x.BDT_cmb > 0.831497)
    bdt_prc = Cut(lambda x: x.BDT_prc > 0.480751)
    bdt = bdt_cmb & bdt_prc
    sign_MC = read_root(sign_MC_path, "ETOS")
    sign_MC = bdt.apply(sign_MC)

    total_n = len(sign_MC)
    brem_0 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity == 0)
    brem_1 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity == 1)
    brem_2 = Cut(lambda x: x.L1_BremMultiplicity + x.L2_BremMultiplicity >= 2)

    f0 = brem_0.get_entries(sign_MC) / total_n
    f1 = brem_1.get_entries(sign_MC) / total_n
    f2 = brem_2.get_entries(sign_MC) / total_n

    utnr.dump_json([f0, f1, f2], json_path)

    return f0, f1, f2


def get_signal_ee(name, preffix, year, trigger):
    scale_reader = CacheMSReader()

    all_mu    = scale_reader.get_scale("mu")
    dmu_value = all_mu.loc[year, f"v_{trigger}"]
    dmu_error = all_mu.loc[year, f"e_{trigger}"]
    all_sg    = scale_reader.get_scale("sg")
    ssg_value = all_sg.loc[year, f"v_{trigger}"]
    ssg_error = all_sg.loc[year, f"e_{trigger}"]

    all_br   = scale_reader.get_scale("br")
    r0_value = all_br.loc[f"{trigger}_{year}", "v_0"]
    r0_error = all_br.loc[f"{trigger}_{year}", "e_0"]
    r1_value = all_br.loc[f"{trigger}_{year}", "v_1"]
    r1_error = all_br.loc[f"{trigger}_{year}", "e_1"]
    r2_value = all_br.loc[f"{trigger}_{year}", "v_2"]
    r2_error = all_br.loc[f"{trigger}_{year}", "e_2"]

    dmu = zfit.Parameter(f"dmu_ee_{preffix}", dmu_value, -50, 50)
    ssg = zfit.Parameter(f"ssg_ee_{preffix}", ssg_value, 0.01, 3)
    r0  = zfit.Parameter(f"r0_ee_{preffix}" , r0_value , 0.01, 3)
    r1  = zfit.Parameter(f"r1_ee_{preffix}" , r1_value , 0.01, 3)
    r2  = zfit.Parameter(f"r2_ee_{preffix}" , r2_value , 0.01, 3)

    constraints = {
        dmu.name: [dmu_value, dmu_error],
        ssg.name: [ssg_value, ssg_error],
        r0.name: [r0_value, r0_error],
        r1.name: [r1_value, r1_error],
        r2.name: [r2_value, r2_error],
    }

    obs = zfit.Space("B_M", limits=(4500, 6000))

    dscbs = []
    for brem_category in range(3):
        dscb = load_signal_ee_brem(preffix, brem_category, obs, year, trigger, dmu, ssg)
        dscbs.append(dscb)

    f0, f1, f2 = get_br_frac()

    f0_corrected = zfit.param.ComposedParameter(
        f"f0_corrected_{preffix}",
        lambda p: f0 * p["r0"] / (f0 * p["r0"] + f1 * p["r1"] + f2 * p["r2"]),
        params={"r0": r0, "r1": r1, "r2": r2},
    )
    f1_corrected = zfit.param.ComposedParameter(
        f"f1_corrected_{preffix}",
        lambda p: f1 * p["r1"] / (f0 * p["r0"] + f1 * p["r1"] + f2 * p["r2"]),
        params={"r0": r0, "r1": r1, "r2": r2},
    )

    total_ee_shape = zfit.pdf.SumPDF(dscbs, [f0_corrected, f1_corrected], name=name)
    return total_ee_shape, constraints

def get_signal_mm(name, preffix, year, trigger):
    scale_reader = CacheMSReader()
    all_mu = scale_reader.get_scale("mu")
    dmu_value = all_mu.loc[f"{year}", f"v_{trigger}"]
    dmu_error = all_mu.loc[f"{year}", f"e_{trigger}"]
    all_sg = scale_reader.get_scale("sg")
    ssg_value = all_sg.loc[f"{year}", f"v_{trigger}"]
    ssg_error = all_sg.loc[f"{year}", f"e_{trigger}"]

    dmu = zfit.Parameter(f"dmu_mm_{preffix}", dmu_value, -50, 50)
    ssg = zfit.Parameter(f"ssg_mm_{preffix}", ssg_value, 0.01, 3)

    constraints = {dmu.name: [dmu_value, dmu_error], ssg.name: [ssg_value, ssg_error]}

    obs = zfit.Space("B_M", limits=(5180, 5600))
    mu  = zfit.Parameter(f"mu_DSCB_mm_{preffix}", 5250, 5180, 5600)
    _mu = zfit.param.ComposedParameter(f"_mu_DSCB_mm_{preffix}", lambda p: p["mu"] + p["dmu"], params={"mu": mu, "dmu": dmu})

    sigma = zfit.Parameter(f"sigma_DSCB_mm_{preffix}", 30, 0, 100)
    _sigma = zfit.param.ComposedParameter(
        f"_sigma_DSCB_mm_{preffix}", lambda p: p["sigma"] * p["ssg"], params={"sigma": sigma, "ssg": ssg}
    )

    alphal = zfit.Parameter(f"alphal_DSCB_mm_{preffix}", 1, 0, 10)
    nl = zfit.Parameter(f"nl_DSCB_mm_{preffix}", 1, 0, 100)
    alphar = zfit.Parameter(f"alphar_DSCB_mm_{preffix}", 1, 0, 10)
    nr = zfit.Parameter(f"nr_DSCB_mm_{preffix}", 1, 0, 100)
    DSCB_mm = zfit.pdf.DoubleCB(
        obs=obs,
        mu=_mu,
        sigma=_sigma,
        alphal=alphal,
        nl=nl,
        alphar=alphar,
        nr=nr,
        name=name,
    )

    pickle_path = get_project_root() + "data/signal_shape_mm/latest/fit_Bu2Kmm_MC_2018_ETOS.pickle"
    DSCB_mm = load_pdf(pickle_path, DSCB_mm, preffix)

    for param in [mu, sigma, alphal, nl, alphar, nr]:
        param.floating = False

    return DSCB_mm, constraints

def get_signal_shape(name='no_name', preffix='', year="2018", trigger="ETOS"):
    if trigger in ["ETOS", "GTIS"]:
        return get_signal_ee(name, preffix, year, trigger)
    elif trigger == "MTOS":
        return get_signal_mm(name, preffix, year, trigger)
    else:
        raise ValueError(f"Unknown trigger: {trigger}")
