from setuptools import setup, find_packages

import glob

setup(
        name            ="rx_hqm",
        version         ='0.0.8',
        description     ='Project used to extract fitting model in high-q2 bin',
        packages        = ['hqm/model', 'hqm/part_reco', 'hqm/tools', 'hqm_data/pars', 'hqm_data'],
        package_data    = {'hqm_data' : ['*.json'], 'hqm_data/pars' : ['*.json']},
        package_dir     = {'' : 'src'},
        install_requires= open('requirements.txt').read()
        )

