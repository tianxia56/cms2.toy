# cms2.toy

## Requirements
- Docker
- selscan v2.0 https://github.com/szpiech/selscan

## Overview
This code generates haplotype (hap) files using cosi2 [cosi2 documentation](https://software.broadinstitute.org/mpg/cosi2/cosidoc.html).

## Instructions

1. Set up env:
    ```sh
    docker run -it -v $(pwd):/home quay.io/ilya_broad/dockstore-tool-cosi2 /bin/bash
    cd home
    ```
or run on cluster:

#Locate a dir and download container
```
cd workingdir/
apptainer build cosi.sif docker://docker.io/tx56/cosi
```

#mount cosi to pwd and run cosi
```
apptainer exec --bind $(pwd):/home cosi.sif /bin/bash
```
 
2. Run the `mk-tpeds.sh` to generate hap files.

3. By default, the script runs 1000 iterations. The demographic model and meta-information are defined in `sel.demo.par`.

4. Put all scripts in the same folder, iterate sim.id over the simulations to generate scores for the selected population (pop1):
    ```sh
    python make-all-scores.py <sim.id> <pop1> <pop2>
    ```
    e.g. one command to rule them all:
   ```sh
    python make-all-scores.py hap.0000 1 2
   ```
the operation order is mk-fst.py, mk-freqs.py, mk-selscans.py, mk-delihh-merge.py, make-all-scores.py.

5. After generating selected and neutral haplotypes, non-repeatedly choose 30 selected and randomly choose 1000 neutral haplotypes to normalized, replace the unnormalized selscan scores with normalized ones by `compu_norm.R`.

6. `add-isafe.py` was after the normalization. the orders do not matter much.

7. add control selection coefficient and sweep ages to plot joint distribution of derfreq, s, and LD scores

   `control-s-tpeds.sh` >>> `control-s-derfreq.sh` >>> `control-s-ldscore.py`
   
