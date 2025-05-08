# pLHE to MINIAOD Toolkit

## Description

This repository contains a series of CMSSW config files to run MC steps from pLHE to MINIAOD.

Also included is a script to obtain the available PREMIX files from a given dataset.

## Usage

The scripts are to be run in sequence to complete all the steps from pLHE to MINIAOD.

1. **LHE to ROOT**: `LHE2GEN_2023C.py`
    ```bash
    # Uses JJY_TPS_test.lhe as the source.
    cmsRun LHE2GEN_2023C.py
    ```
2. **GEN, SIM**: `GEN2SIM_2023C.py`
    ```bash
    cmsRun GENSIM_2023C.py
    ```
3. **DIGI, L1, RAW, HLT**: `SIM2HLT_2023C.py`
    ```bash
    cmsRun SIM2HLT_2023C.py
    ```
4. **RECO**: `RECO_2023C.py` (AOD file is produced)
    ```bash
    cmsRun RECO_2023C.py
    ```
5. **MINIAOD**: `SKIM_2023C.py` (MINIAOD file is produced)
    ```bash
    cmsRun SKIM_2023C.py
    ```

## Regenerating the Scripts Using `cmsDriver.py`

1. `cd` into a `CMSSW_13_0_20/src` and set up the CMSSW environment:
   ```bash
   cmsenv
   ```

2. Use this command to generate the `LHE2GEN_2023C.py`
    ```bash
    cmsDriver.py Configuration/Generator/python/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py \
    --python_filename LHE2GEN_2023C.py\
    --filein file:JJY_TPS_test.lhe\
    --fileout file:JJY_TPS_GEN_2023C_test.root\
    --conditions 130X_mcRun3_2023_realistic_v14\
    --customise Configuration/DataProcessing/Utils.addMonitoring\
    --mc --eventcontent LHE --datatier GEN\
    --step NONE --no_exec -n -1
    ```
3. Use this command to generate the `GEN2SIM_2023C.py`
    ```bash
    cmsDriver.py Configuration/Generator/python/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py \
    --python_filename GENSIM_2023C.py
    --filein file:JJY_TPS_GEN_2023C_test.root\
    --fileout file:JJY_TPS_GENSIM_2023C_test.root\
    --conditions 130X_mcRun3_2023_realistic_v14\
    --beamspot Realistic25ns13p6TeVEarly2023Collision\
    --customise Configuration/DataProcessing/Utils.addMonitoring\
    --mc --eventcontent RAWSIM --datatier GEN-SIM  --nThreads 8 --geometry DB:Extended --era Run3_2023\
    --step GEN,SIM  --no_exec -n -1
    ```
4. Use the `make_premix_non_tape.sh` script to produce a list of PREMIX file available on disks:
    ```bash
    voms-proxy-init -voms cms
    ./make_premix_non_tape.sh "/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer23_130X_mcRun3_2023_realistic_v13-v1/PREMIX" preMix_dataset_2023C.txt
    ```
5. Use the `preMix_dataset_2023C.txt` obtained from the previous step to generate the `SIM2HLT_2023C.py`:
    ```bash
    cmsDriver.py
    --python_filename SIM2HLT_2023C.py\
    --filein file:JJY_TPS_GENSIM_2023C_test.root\
    --fileout file:JJY_TPS_HLT_2023C_test.root\
    --pileup_input filelist:preMix_dataset_2023C.txt\
    --conditions 130X_mcRun3_2023_realistic_v14\
    --procModifiers premix_stage2,siPixelQualityRawToDigi\
    --customise Configuration/DataProcessing/Utils.addMonitoring\ 
    --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW\
    -nThreads 8 --geometry DB:Extended --era Run3_2023 --datamix PreMix\
    --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2023v12 --no_exec -n -1
    ```
6. Use this command to generate the `RECO_2023C.py`:
    ```bash
    cmsDriver.py
    --python_filename RECO_2023C.py\
    --filein file:JJY_TPS_HLT_2023C_test.root\
    --fileout file:JJY_TPS_RECO_2023C_test.root\
    --conditions 130X_mcRun3_2023_realistic_v14\
    --procModifiers siPixelQualityRawToDigi\
    --customise Configuration/DataProcessing/Utils.addMonitoring\
    --mc --eventcontent AODSIM --datatier AODSIM\
    -nThreads 8 --geometry DB:Extended --era Run3_2023\
    --step RAW2DIGI,L1Reco,RECO,RECOSIM --no_exec -n -1\
    ```
7. Use this command to generate the `SKIM_2023C.py`:
    ```bash
    cmsDriver.py
    --python_filename SKIM_2023C.py\
    --filein file:JJY_TPS_RECO_2023C_test.root\
    --fileout file:JJY_TPS_MINIAOD_2023C_test.root\
    --conditions 130X_mcRun3_2023_realistic_v14\
    --customise Configuration/DataProcessing/Utils.addMonitoring \
    --mc --eventcontent MINIAODSIM --datatier MINIAODSIM
    -nThreads 8 --geometry DB:Extended --era Run3_2023\
    --step PAT --no_exec -n -1
    ```
