# pLHE to MINIAOD Toolkit

## Goal:

$J/\psi+J/\psi+\Upsilon(1S)$ pLHE to MINIAOD workflow. Run on `CRAB`

## Dataset Name:

In general, we would adopt the name 

**`QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8`**

> Previously **`JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8`**, changed to meet the suggestions in Ref.[^17] .

We shall start with Run2022C settings and make MC datasets with the following names:

| Data tier   | full name                                                    |
| ----------- | ------------------------------------------------------------ |
| GEN-SIM     | `/QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8/chiw-crab3_Run3Summer22_124X_mcRun3_2022_realistic_v12_MiniAOD_v4_GENSIM-[hash_value]/USER` |
| GEN-SIM-RAW | `/QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8/chiw-crab3_Run3Summer22_124X_mcRun3_2022_realistic_v12_RAW-[hash_value]/USER` |
| AODSIM      | `/QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8/chiw-crab3_Run3Summer22_124X_mcRun3_2022_realistic_v12_AOD-[hash_value]/USER` |
| MINIAODSIM  | `/QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8/chiw-crab3_Run3Summer22_124X_mcRun3_2022_realistic_v12_MiniAOD_v4_MINIAOD-[hash_value]/USER` |

## CMSSW Config from `cmsDriver.py`

### pLHE-GEN-SIM

A framework can be built from this command first [^1][^2][^6]:

```bash
# 2022 in CMSSW_12_4_14_patch3
cmsDriver.py \
Configuration/Generator/python/Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_LHE_pythia8_cff.py \
--mc --no_exec \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM.py \
--eventcontent RAWSIM --step GEN,SIM --datatier GEN-SIM \
--conditions 124X_mcRun3_2022_realistic_v12 \
--beamspot Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 8 --nStreams 8 \
--filein file:JJY_TPS_test.lhe \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM.root

# 2022 post-EE in CMSSW_12_4_14_patch3
cmsDriver.py \
Configuration/Generator/python/Hadronizer_TuneCP5_13TeV_MLM_5f_max4j_LHE_pythia8_cff.py \
--mc --no_exec \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_GENSIM.py \
--eventcontent RAWSIM --step GEN,SIM --datatier GEN-SIM \
--conditions 124X_mcRun3_2022_realistic_postEE_v1 \
--beamspot Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 8 --nStreams 8 \
--filein file:JJY_TPS_test.lhe \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_GENSIM.root

# 2023 in CMSSW_13_0_13

# 2023 post-BPix in CMSSW_13_0_13

# 2024

```

The hadronization fragment shall be modified to be like[^12]:

```python
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *

process.generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,       # Common Pythia8 settings  
        pythia8CP5SettingsBlock,          # CMS CP5 tune for Pythia8 
        pythia8aMCatNLOSettingsBlock,     # Settings for aMC@NLO matching  
        pythia8PSweightsSettingsBlock,    # Settings for parton shower (PS) weights  

        processParameters = cms.vstring(
            "TimeShower:nPartonsInBorn = -1",     # Number of partons in Born process (-1 = auto)  
            "TimeShower:mMaxGamma = 4",           # Maximum photon energy in final-state QED shower (GeV)  
            "PDF:pSet = 7",                       # Use PDF set ID 7   
            
            # Decay mode settings
            "23:onMode = 0",                      # Disable all decays of Z boson  
            "23:onIfMatch = 13 -13",              # Allow only Z to mu+mu-
            "443:onMode = 0",                     # Disable all decays of Jpsi 
            "443:onIfMatch = 13 -13",             # Allow only Jpsi to mu+mu- decay
            "20443:onMode = 0",                   # Disable all decays of Chi_c1  
            "20443:onIfAny = 443",                # Allow Chi_c1 to Jpsi decay  
            "445:onMode = 0",                     # Disable all decays of Chi_c2  
            "445:onIfAny = 443",                  # Allow Chi_c2 to Jpsi decay  
            "10441:onMode=0",                     # Disablealldecaysofh_c
            "10441:onIfAny = 443",                # Allow h_c to Jpsi decay  
            "100443:onMode = 0",                  # Disable all decays of psi(2S)  
            "100443:onIfAny = 443",               # Allow psi(2S) to Jpsi decay 
            "553:onMode = 0",                     # Disable all decays of Upsilon(1S)
            "553:onIfMatch = 13 -13",             # Allow Upsilon(1S) to mu+mu- decay
            "100553:onMode = 0",                  # Disable all decays of Upsilon(2S)
            "100553:onIfMatch = 13 -13",          # Allow Upsilon(2S) to mu+mu- decay
            "200553:onMode = 0",                  # Disable all decays of Upsilon(3S)
            "200553:onIfMatch = 13 -13",          # Allow Upsilon(3S) to mu+mu- decay
        ),

        parameterSets = cms.vstring(
            "pythia8CommonSettings",      
            "pythia8CP5Settings",         
            "pythia8aMCatNLOSettings",    
            "processParameters",          
            "pythia8PSweightsSettings"    
        )
    ),
    comEnergy = cms.double(13600),                    # Collision energy, needs to be same as the setting in HELAC-Onia.
    maxEventsToPrint = cms.untracked.int32(0),        # Do not print event details  
    pythiaHepMCVerbosity = cms.untracked.bool(False), # Disable HepMC event output verbosity  
    pythiaPylistVerbosity = cms.untracked.int32(0),   # Disable Pythia event listing output  
    filterEfficiency = cms.untracked.double(1.0),     # Set filter efficiency to 1.0 (all events pass)  
)
```

### DIGI, L1T, HLT[^1][^2][^4][^6]

```bash
# 2022, CMSSW_12_4_14_patch3
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW.py \
--eventcontent PREMIXRAW --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v12 \
--procModifiers premix_stage2,siPixelQualityRawToDigi --datamix PreMix \
--datatier GEN-SIM-RAW \
--conditions 124X_mcRun3_2022_realistic_v12 \
--beamspot Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--pileup_input filelist:/cvmfs/cms.cern.ch/offcomp-prod/premixPUlist/PREMIX-Run3Summer22DRPremix.txt \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW.root


# 2022 post-EE, CMSSW_12_4_14_patch3
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_RAW.py \
--eventcontent PREMIXRAW --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v14 \
--procModifiers premix_stage2,siPixelQualityRawToDigi --datamix PreMix \
--datatier GEN-SIM-RAW \
--conditions 124X_mcRun3_2022_realistic_postEE_v1 \
--beamspot  Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--pileup_input filelist:/cvmfs/cms.cern.ch/offcomp-prod/premixPUlist/PREMIX-Run3Summer22EEDRPremix.txt \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_GENSIM.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_RAW.root

```

> Very careful with the CMSSW release here! Later releases have removed the `HLT:2022v12` settings at `cmsDriver.py`-level.

Here we are using the pileup files obtained via `cvmfs`. A more flexible way to do it is using this script to obtain the pileup files available sites:

```bash
wget https://raw.githubusercontent.com/FNALLPC/lpc-scripts/refs/heads/master/get_files_on_disk.py
python3 get_files_on_disk.py -a T2_CH_CERN T1_US_FNAL_Disk -o PREMIX.txt DATASET_NAME

```

The favored datasets are

| Era                    | Dataset                                                      |
| ---------------------- | ------------------------------------------------------------ |
| Run2022                | `/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX` |
| Run2023C               | `/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer23_130X_mcRun3_2023_realistic_v13-v1/PREMIX` |
| Run2023D ("post-BPix") | `/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer23BPix_130X_mcRun3_2023_realistic_postBPix_v1-v1/PREMIX` |
| Run2024                | `/Neutrino_E-10_gun/RunIIISummer24PrePremix-Premixlib2024_140X_mcRun3_2024_realistic_v26-v1/PREMIX` |
| Run2025 (?)            | (No PREMIX dataset so far.)                                  |

> The datasets above are actually inferred from the lists in `cvmfs`.



### RECO[^1][^2][^6][^12]

```bash
# 2022
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RECO.py \
--eventcontent AODSIM --step RAW2DIGI,L1Reco,RECO,RECOSIM \
--procModifiers siPixelQualityRawToDigi --datatier GEN-SIM-RAW \
--conditions 124X_mcRun3_2022_realistic_v12 \
--beamspot Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_AOD.root

# 2022 post-EE
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_RECO.py \
--eventcontent AODSIM --step RAW2DIGI,L1Reco,RECO,RECOSIM \
--procModifiers siPixelQualityRawToDigi --datatier GEN-SIM-RAW \
--conditions 124X_mcRun3_2022_realistic_postEE_v1 \
--beamspot Realistic25ns13p6TeVEarly2022Collision \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_RAW.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22EE_AOD.root
```

### MINIAOD[^1][^2][^4][^6][^12]

```bash
# 2022, CMSSW_13_0_13
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_SKIM.py \
--eventcontent MINIAODSIM --step PAT \
--datatier MINIAODSIM \
--conditions 124X_mcRun3_2022_realistic_v12 \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_AOD.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_MiniAOD.root

# 2022 post-EE, CMSSW_13_0_13
cmsDriver.py \
--python_filename JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RECO.py \
--eventcontent MINIAODSIM --step PAT \
--datatier MINIAODSIM \
--conditions 124X_mcRun3_2022_realistic_v12 \
--era Run3 --geometry DB:Extended -n -1 \
--customise Configuration/DataProcessing/Utils.addMonitoring \
--nThreads 1 --nStreams 1 \
--mc --no_exec \
--filein file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_AOD.root \
--fileout file:JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_MiniAOD.root
```



## `CRAB` Config for Running Generation Steps Above

On `CRAB`, running CMSSW config with pLHE input could mean a bit more trouble, especially when we have A LOT of pLHE to process and we are adding PU into consideration.

The first issue is that pLHE could become too large to be transferred to the `CRAB` input sandbox for later processing. In our case, it is \~ 900k events split into \~ 9k files with a total size of \~ 1.8GB, far exceeding the 100MB limit of `CRAB`[^9]. This demands that we do not include pLHE files as inputs in CRAB config, but rather, handle the pLHE file at where they are directly accessible.

For the `GEN-SIM ` step, we are setting the input file source with the PFN to our CERNBox, adding all files into the list of files to be processed, and leaving the job splitting to CRAB. The produced data files will be mostly kept at `T2_CN_Beijing` .

> Very careful here! There have been reports on faulty handling of LHE event ranges.[^15] This was only recently fixed and a section in crab config seems to be required for the thing to work:
>
> ```python
> config.section_("General")
> config.General.instance = 'preprod'
> ```
>
> Yet from recent tests, we actually found that this declaration was not needed. See this testing dataset at `DAS` query:
>
> ```bash
> file dataset=/JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER
> ```
>
> The size of the files do differ, indicating that the splitting was indeed done strictly.
>
> Short summary: just go ahead with the LHE files!

For the `GEN-SIM ` and `DIGI-L1T-HLT` steps, we prefer conducting them only at `T2_CH_CERN`. For the former one, since the LHE files are at `T3_CH_CERNBOX`, running the tasks at `T2_CH_CERN` seems the safest way to do it. For the latter one, it is because `T2_CH_CERN` has an abundant supply of `PREMIX` files and we would like to avoid frequently transferring the pileup samples.[^9]

## Managing Intermediary Files

The intermidiary files can only be manually removed.

Previously, we have generated `/JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER`, which was only a short test. To remove it, well...

```bash
crab setfilestatus --dataset=/JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER --status=INVALID
crab setdatasetstatus --dataset=/JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER --status=INVALID
```

The first command sets all those files as invalid. The second one sets the dataset itself as invalid. What remains to be done is removing all existing files via `xrdfs` .

The first thing to do will be retrieving the LFN of all dataset files. 

```bash
dasgoclient --query="file status=INVALID dataset=/JpsiJpsiY1S_TPS_to_6Mu_13p6TeV_HELAC_Onia2_TuneCP5_pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER instance=prod/phys03" > tmp_GS_to_rm.txt
```

> Took me a while to figure out the right command to use! The `instance=prod/phys03` parameter is taken from Ref. [^19]. Apparently I was not the first one to be puzzled with this... The `status=INVALID` command is there to avoid mistakenly removing some other data files.

Check the `tmp_GS_to_rm` with your favourite editor or just `less`, and then proceed to remove with `xrdfs` command:

```bash
cat tmp_GS_to_rm.txt | xargs -I {} xrdfs xrootd-cms.infn.it rm "{}"
```

> The "`xrootd-cms.infn.it`" specification is picked since I am working at Beijing. The workbook[^20] suggests using `cmsxrootd.fnal.gov` for accessing from the US and `cms-xrd-global.cern.ch` as the "global redirector".


**References**:

[^1]:  `cmsDriver.py` hands-on guide from the 17th (?) CMS Induction Event (Feb. 2025, @ CERN), by Phat Srimanobhas (for `cmsDriver.py` general config and `PreMix` configuration.): https://phat-srimanobhas.gitbook.io/cmsinductionwinter2025-cmssw/cmssw-101/cmsdriver

[^2]: PdmV suggestions (esp. `cmsDriver.py` command reference for MC in `Run3Summer2022`, `Run3Summer2022EE`, `Run3Summer23`, `Run3Summer23BPix`) : https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun3Analysis

[^3]: A more comprehensive guide: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideSimulation

[^4]: On event mixing for PU simulation: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMixingModule

[^5]: Vertex smearing configurations (for `--beamspot` configurations)(only intended as a list of "what is available", please refer to PdmV suggestions): https://cmssdt.cern.ch/lxr/source/Configuration/StandardSequences/python/VtxSmeared.py 

[^6]: Full chain MC hands-on guide from the 2nd China CMS Winter School (Jan. 2024, @ SYSU), by Zhen Hu and Tongguang Cheng: https://indico.ihep.ac.cn/event/21064/contributions/148451/attachments/75611/93299/FullMC_HandsOn.pdf

[^7]: LXR reference for all sorts of existing `Pythia8ConcurrentHadronizerFilter` fragments: https://cmssdt.cern.ch/lxr/source/Configuration/Generator/python/

[^8]: General crab job reference: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab

[^9]: To run crab jobs with LHE input: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTopic#Running_MC_generation_on_LHE_fil 

[^10]: Another tutorial on running crab jobs with LHE input: https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTutorial#Exercise_5_LHE)

[^11]: PdmV suggestions on MC tuning and PDFs: https://cms-pdmv.gitbook.io/project/mccontact/info-for-mc-production-for-run3-campaigns
[^12]: HELAC-Onia 2.7.6 production and further simulation tutorial, from private communication with Yiyang Zhao.
[^13]: A CMS Talk post which might be useful for configuring "sequential MC production". https://cms-talk.web.cern.ch/t/crab-not-accepting-input-dataset-from-fnal-lpc-storage-site/18135
[^14]: Notes on using `root://` PFN paths in CMSSW config for input files. https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookXrootdService
[^15]: Notes on splitting pLHE inputs with CRAB jobs: https://cms-talk.web.cern.ch/t/every-crab-job-runs-with-the-same-input-event/2489/9
[^16]: A test run to check the crab config file.  https://cmsweb.cern.ch/crabserver/ui/task/250518_073925%3Achiw_crab_crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-pre02
[^17]: Naming convention for MC datasets. https://cms-pdmv.gitbook.io/project/mccontact/rules-for-dataset-names
[^ 18]: Invalidating unwanted yet published files: https://twiki.cern.ch/twiki/bin/view/CMSPublic/Crab3DataHandling#Changing_a_dataset_or_file_statu
[^19]: On retrieving private MC file list via DAS CLI: https://cms-talk.web.cern.ch/t/problems-to-query-files-of-a-dataset-with-dasgoclient/38302
[^20]: On choosing the redirector of `xrootd` service: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookXrootdService#ReDirector