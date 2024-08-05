import argparse
import glob
import re
import os
import ROOT
from report_to_elog_scans import elog

data_folder = '/home/akumar/vtx_belle2/analysis/beam/2024_07_DESY/data/beam_data/desy'
corry_bin = '/home/akumar/vtx_belle2/corryvreckan/bin/corry'
corry_config_template = 'analysis.conf'
output_dir = '/home/akumar/vtx_belle2/analysis/beam/2024_07_DESY/corry_config_desytb_2024/ana_out'

selected_keys = [
    "AnalysisDUT/Monopix2_0/local_residuals/residualsX",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsX1pix",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsX2pix",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsX3pix",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsY",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsY1pix",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsY2pix",
    "AnalysisDUT/Monopix2_0/local_residuals/residualsY3pix",
    "AnalysisDUT/Monopix2_0/seedChargeVsColAssoc",
    "AnalysisDUT/Monopix2_0/hitMapAssoc",
    "AnalysisDUT/Monopix2_0/clusterChargeAssociated",
    "AnalysisDUT/Monopix2_0/seedChargeAssociated",
    "AnalysisDUT/Monopix2_0/clusterSizeAssociated",
    "AnalysisDUT/Monopix2_0/clusterWidthRowAssociated",
    "AnalysisDUT/Monopix2_0/clusterWidthColAssociated",
    "AnalysisEfficiency/Monopix2_0/pixelEfficiencyMap_trackPos",
    "AnalysisEfficiency/Monopix2_0/chipEfficiencyMap_trackPos",
    "AnalysisEfficiency/Monopix2_0/distanceTrackHit2D",
    "AnalysisEfficiency/Monopix2_0/eTotalEfficiency",
    "AnalysisEfficiency/Monopix2_0/efficiencyColumns",
    "AnalysisEfficiency/Monopix2_0/efficiencyRows",
    "AnalysisDUT/Monopix2_0/rmsxyvsxmym",
    "AnalysisDUT/Monopix2_0/pxqvsxmym",
    "AnalysisDUT/Monopix2_0/npxvsxmym",
    "AnalysisDUT/Monopix2_0/qvsxmym",
    "AnalysisDUT/Monopix2_0/pqxqvsxmym",
]


def make_pdf(filename):
    
    # Open files with reconstructed run data 
    f = ROOT.TFile( filename) 

    pdfName = output_dir + '/' + os.path.splitext( os.path.basename( filename ) )[0] + '.pdf'
    
    c1 = ROOT.TCanvas("c1","",10,10,1100,700)
    c1.SetRightMargin(0.2)
  
    for key in selected_keys: #histofile.GetListOfKeys():

        print(key)
        obj = f.Get(key)
        
        if obj.InheritsFrom("TH1"):
            h1 = obj.Clone()
            c1.Clear()
            c1.cd()
            c1.SetName(key)
            c1.SetTitle(key)
      
            if  h1.InheritsFrom("TH2"): 
                h1.Draw("colz")
            else: 
                h1.Draw()
      
            ROOT.gPad.Modified()
            ROOT.gPad.Update()   
            c1.Print(pdfName+"(","pdf")

        elif obj.InheritsFrom("TEfficiency"):
      
            e  = obj.Clone()
            c1.Clear()
            c1.cd()
            c1.SetName(key)
            c1.SetTitle(key)
            
            if  e.GetDimension() > 1:
                e.Draw("colz")
            else: 
                e.Draw()
      
            ROOT.gPad.Modified()
            ROOT.gPad.Update()   
            c1.Print(pdfName+"(","pdf")

  
    c1.Print(pdfName+")","pdf")
    f.Close()
    return pdfName



parser = argparse.ArgumentParser(description='corry analysis wrapper')
parser.add_argument('-r', help='run number')
parser.add_argument('--start', help='start run number')
parser.add_argument('--stop', help='stop run number')
parser.add_argument('-g', help='geoid number', required=True)
parser.add_argument('-n', help='number of events', default = 50000)
parser.add_argument('-c', help='comment to output file name')

args = parser.parse_args()
if args.r and ( args.start or args.stop):
    print("don't use runNmb and start + stop!")
    exit
elif args.start and not args.stop:
    print('start without stop, not working buddy')
    exit

analyze_single_run = True
if args.start and args.stop:
    analyze_single_run = False

start = 0
stop = 0

if analyze_single_run:
    start = int(args.r)
    stop = int(args.r) + 1
else:
    start = int(args.start)
    stop = int(args.stop) + 1 # in range end is not inclusive, make sure we process last specified run too

for i in range(start, stop):
    current_run = str(i)    
    output_file_name = f'analysis_run{current_run}'

    if args.c:
        output_file_name += '_' + args.c

    pdfName = make_pdf(f'{output_dir}/{output_file_name}.root')