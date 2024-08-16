## Add script to extract efficiency and residuals from analysed root file ##
## @Ajit Kumar, IPHC Strasbourg
## Date: 16/08/2024


import ROOT
import argparse
import glob
import re
import os
import pandas as pd

# numerical calculation
def efficiency_simple(nsel, nall):
  if(nall < 1.):
    return (0., 0.)
  eff = float(nsel) / float(nall)
  lowerErrorEff = eff - ROOT.TEfficiency.ClopperPearson(nall, nsel, 0.683, False)
  upperErrorEff = ROOT.TEfficiency.ClopperPearson(nall, nsel, 0.683, True) - eff
  error = (upperErrorEff + lowerErrorEff) / 2.
  return eff, error, lowerErrorEff, upperErrorEff

def show_efficiency(nsel, nall):
  eff, error, lerr, uerr = efficiency_simple(nsel, nall)
  return f'{eff * 100:.1f}^{{+{uerr * 100:.1f}}}_{{-{lerr * 100:.1f}}} %'


def optimise_hist_gaus(hist):
    peak = hist.GetMaximum()
    mean = hist.GetMean()
    rms = hist.GetRMS()
    halfLeft = hist.FindFirstBinAbove(peak/2.)
    halfRight = hist.FindLastBinAbove(peak/2.)
    center = 0.5 * (hist.GetBinCenter(halfRight) + hist.GetBinCenter(halfLeft))
    fwhm = hist.GetBinCenter(halfRight) - hist.GetBinCenter(halfLeft)
    if fwhm < 2 * hist.GetBinWidth(1):
        print(f'[X] Warning  - FWHM too narrow {center = }, {fwhm = }, {rms = }, {peak = }')
        return None
    fitRange = min(5 * rms, 1.0 * fwhm)
    fcnGaus = ROOT.TF1(f'fcnFitGaus_{hist.GetName()}', 'gaus', center - fitRange, center + fitRange)
    resultPtr = hist.Fit(fcnGaus,'SQN','', center - fitRange, center + fitRange)
    try:
        params = resultPtr.GetParams()
    except ReferenceError:
        print(f'[X] Warning  - Fitting failed with {center = }, {fwhm = }, {rms = }, {peak = }')
        return None
    parErrors = resultPtr.GetErrors()
    mean = params[1]
    sigma = params[2]
    mean_error = parErrors[1]
    sigma_error = parErrors[2]
    return mean, sigma, mean_error, sigma_error

rootfile_folder = 'path/to/ana/rootfile'

parser = argparse.ArgumentParser(description='Post-processing script for corryvreckan')
parser.add_argument('-f', '--infile',help='Output histogram from corry', default="analog-debug.root")
parser.add_argument('-r', help='run number', default = 0)
parser.add_argument('--start', help='run number start', default = 0)
parser.add_argument('--stop', help='run number stop', default = 0)

args = parser.parse_args()

if args.r == 0 and (args.start == 0 or args.stop == 0):
    print("Either use run number or start/stop to give a range of runs to be analyzed.")

if args.r != 0:
    run_start = args.r
    run_stop = args.r
else:
    run_start = args.start
    run_stop = args.stop
print(run_start, run_stop)
data_in_files = glob.glob(rootfile_folder + '/*.root')
# print(data_in_files)
for current_run in range(int(run_start),int(run_stop)+1):
    current_root_file = ''
    for f in data_in_files:
        m = re.search(f'analysis.+run(0*{current_run})', f)
        if m:
            current_root_file = f
    if current_root_file == '':
        print(f'root_files empty for run {current_run}')
        continue

    fname = current_root_file
    print(fname)
    fn = fname.split('_')
    print(fn)
    run_number = fn[7][3:]
    print('run number', run_number)

    # Step 1: Load the .root file
    file = ROOT.TFile(current_root_file)

    # Step 2: Access the AnalysisDUT directory
    analysis_dut_dir = file.Get("AnalysisDUT/Monopix2_0")
    analysis_dut_dir_res = file.Get("AnalysisDUT/Monopix2_0/global_residuals")

    # Step 3: Retrieve the hCutHisto histogram
    hCutHisto = analysis_dut_dir.Get("hCutHisto")
    hResX = analysis_dut_dir_res.Get("residualsX")
    hResY = analysis_dut_dir_res.Get("residualsY")

    # efficiency calculation
    nTrack = int(hCutHisto.GetBinContent(1))
    nTrackCutChi2 = int(hCutHisto.GetBinContent(2))
    nTrackCutDUT = int(hCutHisto.GetBinContent(3))
    nTrackCutROI = int(hCutHisto.GetBinContent(4))
    nTrackCutMask = int(hCutHisto.GetBinContent(2))
    nTrackPass = int(hCutHisto.GetBinContent(7))
    nAssociatedCluster = int(hCutHisto.GetBinContent(8)) 
    # print(nTrackPass, nAssociatedCluster) 
    if(nTrackPass==0): continue
    eff, error, lerr, uerr = efficiency_simple(nAssociatedCluster, nTrackPass)
    print(eff, error, lerr, uerr)
    with open(f'efficiency_with_runno.txt', 'a') as f:
        f.write(str(run_number)+'\t'+str(nTrackPass)+'\t'+str(nAssociatedCluster)+'\t'+str(eff)+'\t'+str(error)+'\t'+str(lerr)+'\t'+str(uerr)+'\n')

    # resolution calculation
    meanx, sigmax, errmeanx, errsigmax = optimise_hist_gaus(hResX)
    meany, sigmay, errmeany, errsigmay = optimise_hist_gaus(hResY)
    mean=(meanx+meany)/2.0
    sigma=(sigmax+sigmax)/2.0
    errmean=(errmeanx+errmeanx)/2.0
    errsigma=(errsigmax+errsigmax)/2.0
    # print(meanx, sigmax, errmeanx, errsigmax)
    print(mean, sigma, errmean, errsigma)
    with open(f'residuals_with_runno.txt', 'a') as f:
        f.write(str(run_number)+'\t'+str(mean)+'\t'+str(errmean)+'\t'+str(sigma)+'\t'+str(errsigma)+'\n')
