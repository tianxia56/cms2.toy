# cms2.toy

## Requirements
- Docker
- selscan v2.0 https://github.com/szpiech/selscan

## Overview
This code generates haplotype (hap) files using cosi2 [cosi2 documentation](https://software.broadinstitute.org/mpg/cosi2/cosidoc.html).

## Instructions

1. Use Docker to set up the environment:
    ```sh
    docker run -it -v $(pwd):/home quay.io/ilya_broad/dockstore-tool-cosi2 /bin/bash
    cd home
    ```
 
2. Run the `mk-tpeds.sh` script.

3. By default, the script runs 1000 iterations. The demographic model and meta-information are defined in `sel.demo.par`.

4. Iterate over the simulations to generate scores for the selected population:
    ```sh
    python make-all-scores.py <sim.id> <pop1> <pop2>
    ```
    e.g.:
   ```sh
    python make-all-scores.py hap.0000 1 2
   ```
   
