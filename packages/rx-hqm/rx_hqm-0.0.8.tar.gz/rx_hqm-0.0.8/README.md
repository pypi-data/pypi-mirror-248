# Installation

``` shell
pip install -e .
```
create symbolic links in the project root directory:

``` shell
ln -s /publicfs/ucas/user/qi/public/RK/high_q2_yield_study/data
ln -s /publicfs/ucas/user/qi/public/RK/high_q2_yield_study/root_sample
```

# Usage
## Mass window
This package provide the pdf in following mass window

+ (4500, 6000) MeV for electron
+ (5180, 5600) MeV for muon

**Use same mass window as this**, some parameters are mass-window dependent
## Get shape
Only 2018 ETOS for electron and 2018 MTOS for muon are available for now

``` python
import hqm #import the package

# muon signal shape and constriaints
signal_shape_mm, constraints = get_signal_shape(year="2018", trigger="MTOS")

#electron signal shape and constraints
signal_shape_ee, constraints = get_signal_shape(year="2018", trigger="ETOS")
#rare part-reco B0 -> K* ee
Bd2Ksee_shape = get_Bd2Ksee_shape()
#rare part-reco B+ -> K* ee
Bu2Ksee_shape = get_Bu2Ksee_shape()
#resonant part-reco + psi2S K, ratio fixed
part_reco_shape = get_part_reco()
```



