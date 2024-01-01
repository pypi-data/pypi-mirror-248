from hqm.tools.scales import eff_calc

import pprint
import utils_noroot as utnr

#-------------------------------------
def test_simple():
    calc  = eff_calc()
    calc.out_dir = 'tests/eff_calc'
    d_eff = calc.get_efficiencies()

    utnr.dump_json(d_eff, './efficiency.json')
#-------------------------------------
if __name__ == '__main__':
    test_simple()

