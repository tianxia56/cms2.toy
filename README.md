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
 
2. Run the `mk-tpeds.sh` to generate hap files.

3. By default, the script runs 1000 iterations. The demographic model and meta-information are defined in `sel.demo.par`.

4. Iterate sim.id over the simulations to generate scores for the selected population (pop1):
    ```sh
    python make-all-scores.py <sim.id> <pop1> <pop2>
    ```
    e.g.:
   ```sh
    python make-all-scores.py hap.0000 1 2
   ```
   
