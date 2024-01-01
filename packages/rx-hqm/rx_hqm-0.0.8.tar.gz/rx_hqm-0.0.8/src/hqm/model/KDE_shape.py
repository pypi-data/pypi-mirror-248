from hqm.tools.utility   import get_project_root
from hqm.tools.utility   import read_root
from hqm.tools.Cut       import Cut
from importlib.resources import files
from logzero             import logger

import os
import zfit
import glob
import ROOT
import numpy
import awkward      as ak
import utils_noroot as utnr

#------------------------------------------
class data:
    ntp_vers = 'v10.21p2'
#------------------------------------------
def get_casdir_paths(trigger, dset, kind_dir):
    cas_dir = os.environ['CASDIR']
    if   dset == 'r1':
        file_wc_1 =  f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2011_{trigger}/*.root'
        file_wc_2 =  f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2012_{trigger}/*.root'

        l_file_wc = [file_wc_1, file_wc_2]
    elif dset == 'r2p1':
        file_wc_1 =  f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2011_{trigger}/*.root'
        file_wc_2 =  f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2012_{trigger}/*.root'

        l_file_wc = [file_wc_1, file_wc_2]
    elif dset == '2017':
        l_file_wc = [f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2017_{trigger}/*.root']
    elif dset == '2018':
        l_file_wc = [f'{cas_dir}/tools/apply_selection/signal_fit/{kind_dir}/{data.ntp_vers}/2018_{trigger}/*.root']
    else:
        logger.error(f'Invalid dataset: {dset}')
        raise

    l_file_path = []
    for file_wc in l_file_wc:
        l_file_path += glob.glob(file_wc)

    if len(l_file_path) == 0:
        logger.error(f'No files found in: {l_file_wc}')
        raise

    return l_file_path
#------------------------------------------
def read_from_casdir(q2, trigger, dset, kind_dir):
    hqm_data  = files('hqm_data')
    json_path = f'{hqm_data}/pars/{kind_dir}_{q2}_{trigger}_{dset}.json'
    if os.path.isfile(json_path):
        logger.info(f'Reloading data from: {json_path}')
        l_mass = utnr.load_json(json_path)
        return numpy.array(l_mass) 


    l_file_path = get_casdir_paths(trigger, dset, kind_dir)

    rdf      = ROOT.RDataFrame(trigger, l_file_path)
    arr_mass = rdf.AsNumpy(['B_M'])['B_M']

    logger.info(f'Caching data to: {json_path}')
    utnr.dump_json(arr_mass.tolist(), json_path)

    return arr_mass
#------------------------------------------
def get_data(q2, kind_dir):
    data_path  = get_project_root() + f"root_sample/v5/{kind_dir}/v10.21p2/2018_ETOS/{q2}_nomass.root"
    data_name  = data_path.replace('/', '_').replace('.', '_p_')
    json_path  = files('hqm_data').joinpath(f'pars/{data_name}.json')
    if not os.path.isfile(json_path):
        data_array = read_root(data_path, "ETOS")
        bdt_cmb    = Cut(lambda x: x.BDT_cmb > 0.831497)
        bdt_prc    = Cut(lambda x: x.BDT_prc > 0.480751)
        bdt        = bdt_cmb & bdt_prc
        data_array = bdt.apply(data_array)
        data_array = ak.to_numpy(data_array.B_M)

        utnr.dump_json(data_array.tolist(), json_path)
    else:
        logger.debug(f'Loading KDE data from: {json_path}')
        l_data     = utnr.load_json(json_path)
        data_array = numpy.array(l_data)

    return data_array
#------------------------------------------
def get_KDE_shape(obs, kind, q2, name, trigger=None, dset=None, bandwidth=10):
    kind_dir = 'ctrl' if kind == 'jpsi' else kind

    if kind_dir in ['bsph', 'bpk1', 'bpk2']:
        data_array = read_from_casdir(q2, trigger, dset, kind_dir)
    else:
        data_array = get_data(q2, kind_dir)

    zdata = zfit.Data.from_numpy(obs, array=data_array)
    shape = zfit.pdf.KDE1DimFFT(obs=obs, data=zdata, name=name, bandwidth=bandwidth)

    shape.arr_mass = data_array

    return shape
#------------------------------------------

