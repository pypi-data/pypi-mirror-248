import ROOT

#-------------------------------------
def transform_bdt(working_point):
    '''
    Will return BDT score after using RK central analysis' transformation

    Parameters
    ------------
    working_point (float): Working point from TMVA, from -1 to 1

    Returns 
    ------------
    working_point (float): Working point transformed, from 0 to 1 + epsilon  
    '''

    return ((ROOT.TMath.ASin(ROOT.TMath.ASin(working_point)*(2/ROOT.TMath.Pi()))+0.5*ROOT.TMath.Pi()))/3.
#-------------------------------------
