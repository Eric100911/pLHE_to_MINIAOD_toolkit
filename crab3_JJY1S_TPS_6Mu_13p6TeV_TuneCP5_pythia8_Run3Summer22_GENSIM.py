from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 1

config.Data.outputPrimaryDataset = 'QCD-TPS-JPsiJPsiUpsilon1Sto6Mu_TuneCP5_13p6TeV_helaconia2-pythia8'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1500
config.Data.totalUnits  = 972249

config.Data.publication = True
config.Data.outputDatasetTag = 'crab3_JJY1S_TPS_6Mu_13p6TeV_TuneCP5_pythia8_Run3Summer22_GENSIM' # Change here with your lxplus name

config.section_('Site')
#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T2_CN_Beijing'
config.Data.outLFNDirBase = '/store/user/chiw/MC_JJY1S_TPS_2022/'  # Change here with your lxplus name
