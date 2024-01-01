from hqm.model         import get_part_reco
from hqm.model         import get_rare_shape
from hqm.model         import get_signal_shape
from hqm.tools.utility import get_project_root
from logzero           import logger
from zutils.plot       import plot   as zfp

import matplotlib.pyplot as plt
import zutils.utils      as zut

import numpy             as np
import os

#------------------------------------
def plot(shape, label, mass_window=(4500, 6000), d_const=None):
    plot_dir = 'output/tests/pdf'
    os.makedirs(plot_dir, exist_ok=True)

    obj   = zfp(data=shape.arr_mass, model=shape)
    obj.plot(nbins=50)

    logger.info(f"saving plot to {plot_dir}/{label}.pdf")
    plt.savefig(f'{plot_dir}/{label}.pdf')
    plt.close()

    zut.print_pdf(shape, txt_path=f'{plot_dir}/{label}.txt', d_const=d_const)
#------------------------------------
def test_part_reco():
    pdf= get_part_reco(preffix='prc', name='pr shape')
    pdf.arr_mass = pdf.create_sampler(n=10000, fixed_params=False)
    plot(pdf, "part_reco")
#------------------------------------
def test_BsPhiee():
    pdf = get_rare_shape(year='2018', trigger='ETOS', name='Bsph shape', kind='bsph')
    plot(pdf, "BsPhiee")
#------------------------------------
def test_BpK1ee():
    pdf = get_rare_shape(year='2018', trigger='ETOS', name='BpK1 shape', kind='bpk1')
    plot(pdf , "BpK1ee")
#------------------------------------
def test_BpK2ee():
    pdf = get_rare_shape(year='2018', trigger='ETOS', name='BpK2 shape', kind='bpk2')
    plot(pdf , "BpK2ee")
#------------------------------------
def test_Bd2Ksee():
    pdf = get_rare_shape(year='2018', trigger='ETOS', name='BdKs shape', kind='bdks')
    plot(pdf, "Bd2Ksee")
#------------------------------------
def test_Bu2Ksee():
    pdf = get_rare_shape(year='2018', trigger='ETOS', name='Bukp shape', kind='bpks')
    plot(pdf, "Bu2Ksee")
#------------------------------------
def test_signal_shape_mm():
    pdf, constraints = get_signal_shape(name='sig_mm', preffix='mm_18_tos', year="2018", trigger="MTOS")
    pdf.arr_mass = pdf.create_sampler(n=10000)

    plot(pdf, "signal_shape_mm", (5180, 5600), d_const=constraints)
#------------------------------------
def test_signal_shape_ee():
    pdf, constraints = get_signal_shape(name='sig_ee', preffix='ee_18_tos', year="2018", trigger="ETOS")
    pdf.arr_mass = pdf.create_sampler(n=10000)
    plot(pdf, "signal_shape_ee", (4500, 6000), d_const=constraints)
#------------------------------------
def main():
    test_part_reco()
    test_signal_shape_mm()
    test_signal_shape_ee()
    test_BpK2ee()
    test_BpK1ee()
    test_BsPhiee()
    test_Bu2Ksee()
    test_Bd2Ksee()
#------------------------------------
if __name__ == '__main__':
    main()

