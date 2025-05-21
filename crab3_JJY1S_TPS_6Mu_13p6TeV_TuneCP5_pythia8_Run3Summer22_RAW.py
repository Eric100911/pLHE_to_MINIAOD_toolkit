from CRABClient.UserUtilities import config
config = config()

config.section_('General')
config.General.requestName = 'crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 1
config.JobType.maxJobRuntimeMin = 450
config.JobType.maxMemoryMB = 3500         # crab submit --dryrun gave estimation of 2981MB; extra 500MB as margin
config.JobType.outputFiles = ['JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_RAW.root']

config.section_('Data')
config.Data.inputDataset = '/QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8/chiw-crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM-b97cb38d4172304bce7c88d7a279c79c/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = True
config.Data.outLFNDirBase = '/store/user/chiw/MC_JJY1S_TPS_2022/'  # Change here with your lxplus name
config.Data.outputDatasetTag = 'crab3_Run3Summer22_124X_mcRun3_2022_realistic_v12_RAWSIM' # Change here with your lxplus name

config.section_('User')
config.section_('Site')
#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T2_CN_Beijing'
