#!/bin/env python3

import sys, os, json,argparse
import math

parser = argparse.ArgumentParser(description='Post-processing script for corryvreckan')
parser.add_argument('-f', '--file',help='Output histogram from corry', default="analog-debug.root")
parser.add_argument('-p', '--print',help='Print in PDF file', default=None)
parser.add_argument('-d', '--detector',help='Print in PDF file', default='CE65_6')
parser.add_argument('-n', '--nrefs',help='Number of reference MIMOSA26 planes', default=6, type=int)
parser.add_argument('--charge-max', dest='CHARGE_MAX', help='Max charge for histograms binning', default=256, type=float)
parser.add_argument('--charge-binwidth',dest='CHARGE_BINWIDTH', help='Charge bin width for histograms binning', default=1, type=float)
parser.add_argument('--fit-range',dest='GAUS_FIT', help='Fitting range for gaussian distribution, ratio as FWHM', default=1.0, type=float)
parser.add_argument('--noisy-freq', dest='NOISY_FREQUENCY', help='Threshold of hit frequency to identify noisy pixels', default=0.001, type=float)
parser.add_argument('--roi', help='Select ROI from Correlation by FWHM method', default=False,action='store_true')

args = parser.parse_args()

import ROOT
from plot_util import *

if(args.print is None):
  args.print = args.file.replace('.root','.pdf')
elif not args.print.endswith('.pdf'):
  args.print = args.print + '.pdf'

ALICEStyle()
ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetLineWidth(1)
ROOT.gStyle.SetOptTitle(1)
ROOT.gStyle.SetOptStat(0)

CE65_SUBMATRIX_EDGE = [21, 42, 64]

class CorryPainter(Painter):
  """ROOT Painter for histograms output from corryvreckan
  Support modules:
    - ClusteringSpatial
    - ClusteringAnalog
    - Correlations
    - AnalysisDUT
    - AnalysisCE65
    - Tracking4D
    - DUTAssociation
    - AlignmentDUTResidual
  """
  def __init__(self, canvas, printer, **kwargs):
    super().__init__(canvas, printer, **kwargs)
  # def select_roi(self, hitmap, bin_width=1, roi_scale=1.5, suffix=''):
  def select_roi(self, hitmap, bin_width=1, roi_scale=1.5, suffix=''):
    """ Select trigger region as ROI
    """
    hitx = self.new_obj(hitmap.ProjectionX(f'{hitmap.GetName()}{suffix}_px'))
    hitx.SetTitle(f'{suffix} - cluster map projection X')
    hitx.Rebin(int(bin_width // hitx.GetBinWidth(1)))
    self.DrawHist(hitx, optGaus=True, optStat=True)
    x_width, x_center = self.estimate_fwhm(hitx)
    hity = self.new_obj(hitmap.ProjectionY(f'{hitmap.GetName()}{suffix}_py'))
    hity.SetTitle(f'{suffix} - cluster map projection Y')
    hity.Rebin(int(bin_width // hity.GetBinWidth(1)))
    self.DrawHist(hity, optGaus=True, optStat=True)
    y_width, y_center = self.estimate_fwhm(hity)
    xlower = math.floor(x_center - roi_scale * x_width)
    xupper = math.ceil(x_center + roi_scale * x_width)
    ylower = math.floor(y_center - roi_scale * y_width)
    yupper = math.ceil(y_center + roi_scale * y_width)
    return xlower, xupper, ylower, yupper
  # End - class CorryPainter

c = ROOT.TCanvas('cQA','Corry Performance Figures',2560, 1440)
c.SetMargin(0.15, 0.1, 0.15, 0.1)
c.Draw()
paint = CorryPainter(c, args.print, nx=4, ny=3, gausFitRange=args.GAUS_FIT,
  marginTop=0.08)
paint.PrintCover()

corryHist = ROOT.TFile(args.file)

eventModule = "EventLoaderEUDAQ2"
clusterMIMOSA26Module = "ClusteringSpatial"
clusterModule = "ClusteringAnalog"
corrModule = "Correlations"
analysisModule = "AnalysisDUT"
trackingModule = "Tracking4D"
associationModule = 'DUTAssociation'
alignDUTModule = "AlignmentDUTResidual"
detector = args.detector

def DrawEventLoaderEUDAQ2(self, dirEvent):
  htmp = dirEvent.Get('eudaqEventStart')
  self.N_EVENT = htmp.GetEntries()
  return None
CorryPainter.DrawEventLoaderEUDAQ2 = DrawEventLoaderEUDAQ2
paint.DrawEventLoaderEUDAQ2(corryHist.Get(eventModule).Get('MIMOSA26_0'))

def DrawClusteringAnalog(self, dirCluster, nextPage=True, suffix=''):
  # Init
  if(nextPage):
    self.pageName = f"ClusteringAnalog - {detector}"
  # Drawing
  hMap = dirCluster.Get("clusterPositionLocal")
  self.DrawHist(hMap, option="colz")
  self.draw_text(0.55, 0.92, 0.95, 0.98, f'Total N_{{cluster}} : {hMap.GetEntries():.0f}', font=62, size=0.05).Draw("same")
    # Noisy pixel
  hHitFreq = self.new_obj(ROOT.TH1F(f'hHitFreq{suffix}','Hitmap by cluster (frequency);Frequency;# pixels',10000,0.,1.0))
  pavePixel = self.draw_text(0.7, 0.6, 0.85, 0.80)
  nNoisy = 0
  print('>>> Mask creation by output of ClusteringAnalog')
  for iy in range(1,hMap.GetNbinsY()+1):
    for ix in range(1,hMap.GetNbinsX()+1):
      clusterCount = hMap.GetBinContent(ix, iy)
      clusterFreq = clusterCount / self.N_EVENT
      hHitFreq.Fill(clusterFreq)
      if(clusterFreq > args.NOISY_FREQUENCY):
        self.add_text(pavePixel, f'({ix-1}, {iy-1}) - {clusterFreq:.1e} [{clusterCount:.0f}]', size=0.025)
        nNoisy += 1
        print(f'p\t{ix-1}\t{iy-1} # {clusterFreq:.1e} [{clusterCount:.0f}]')
  self.DrawHist(hHitFreq, optLogY=True, optLogX=True, optStat=True)
  hHitFreq.SaveAs('noisy_mask.root') # DEBUG
  nNoHits = hHitFreq.GetBinContent(hHitFreq.FindBin(0.))
  paveStat = self.draw_text(0.2, 0.2, 0.42, 0.30)
  self.add_text(paveStat, f'Event loaded : {self.N_EVENT:.0f}')
  self.add_text(paveStat, f'No hits pixels : {nNoHits:.0f}')
  paveStat.Draw('same')
  self.draw_text(0.5, 0.80, 0.85, 0.85, f'Noisy pixels (freq. > {args.NOISY_FREQUENCY}) : {nNoisy}').Draw('same')
  if(nNoisy < 10): pavePixel.Draw('same')

  hSize = dirCluster.Get("clusterSize")
  hSize.GetXaxis().SetRangeUser(0,25)
  self.DrawHist(hSize, "clusterSize", optLogY=True, optStat=True)
  # ROOT.gStyle.SetOptStat(1101)
  # gStyle->SetOptStat(1101)
  # self.DrawHist(hSize, "clusterSize", optLogY=True, optStat=True)

  hSize = dirCluster.Get("clusterCharge")
  hSize.Rebin(int(args.CHARGE_BINWIDTH / hSize.GetBinWidth(1)))
  hSize.GetXaxis().SetRangeUser(-0.05 * args.CHARGE_MAX,args.CHARGE_MAX)
  self.DrawHist(hSize, "clusterCharge", optLogY=True, optStat=True)

  hSize = dirCluster.Get("clusterSeedCharge")
  hSize.Rebin(int(args.CHARGE_BINWIDTH  / hSize.GetBinWidth(1)))
  hSize.GetXaxis().SetRangeUser(0,args.CHARGE_MAX)
  self.DrawHist(hSize, "clusterSeedCharge", optLogY=True, optStat=True)

  hSize = dirCluster.Get("clusterNeighborsCharge")
  hSize.Rebin(int(args.CHARGE_BINWIDTH  / hSize.GetBinWidth(1)))
  hSize.GetXaxis().SetRangeUser(-0.05 * args.CHARGE_MAX, args.CHARGE_MAX)
  self.DrawHist(hSize, "clusterNeighborsCharge", optLogY=True, optStat=True)

  hSize = dirCluster.Get("clusterNeighborsChargeSum")
  hSize.Rebin(int(args.CHARGE_BINWIDTH  / hSize.GetBinWidth(1)))
  hSize.GetXaxis().SetRangeUser(-0.05 * args.CHARGE_MAX,args.CHARGE_MAX)
  self.DrawHist(hSize, "Cluster neighbors charge", optLogY=True, optStat=True)

  hSize = dirCluster.Get("clusterSeedSNR")
  if (hSize): 
    hSize.Rebin(int(1 / hSize.GetBinWidth(1)))
    hSize.GetXaxis().SetRangeUser(0,100)
    hSize.GetYaxis().SetRangeUser(0,hSize.GetMaximum() * 1.2)
    self.DrawHist(hSize, "clusterSeedSNR", optStat=True)
  else:
  	pass
  
  hSize = dirCluster.Get("clusterNeighborsSNR")
  if(hSize): 
    hSize.GetXaxis().SetRangeUser(-3,20)
    self.DrawHist(hSize, "clusterNeighborsSNR", optLogY=False, optStat=True)
  else:
    pass

  hMap = dirCluster.Get("clusterCharge_SeedvsNeighbors")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX,args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterCharge_SeedvsNeighbors", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterSNR_SeedvsNeighbors")
  if (hMap):
    hMap.GetYaxis().SetRangeUser(-1,10)
    self.DrawHist(hMap, "clusterSNR_SeedvsNeighbors", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterCharge_SeedvsNeighborsSum")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterCharge_SeedvsNeighborsSum", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterCharge_SeedvsCluster")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX,args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterCharge_SeedvsCluster", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterSeedSNRvsClusterCharge")
  if (hMap):
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterSeedSNRvsClusterCharge", "colz", False)
  else:
    pass
  
  # Cluster shape
  hSize = dirCluster.Get("clusterShape_SeedCut")
  if (hSize):
    hSize.GetXaxis().SetRangeUser(0,10)
    self.draw_text(0.58, 0.55, 0.85, 0.85, f'Average size: {hSize.GetMean()}')
    self.DrawHist(hSize, "clusterShape_SeedCut", optStat=True)
  else:
    pass

  hMap = dirCluster.Get("clusterShape_Charge_LocalIndex")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-5,5)
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterShape_Charge_LocalIndex", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterShape_Charge_SortedIndex")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(0,10)
    hMap.GetYaxis().SetRangeUser(-0.1 * args.CHARGE_MAX, args.CHARGE_MAX)
    self.DrawHist(hMap, "clusterShape_Charge_SortedIndex", "colz", optNormY=True)
  else:
    pass

  hMap = dirCluster.Get("clusterShape_SNR_LocalIndex")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-5,5)
    self.DrawHist(hMap, "clusterShape_SNR_LocalIndex", "colz", False)
  else:
    pass

  hMap = dirCluster.Get("clusterShape_SNR_SortedIndex")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(0,10)
    self.DrawHist(hMap, "clusterShape_SNR_SortedIndex", "colz", False, optNormY=True)
  else:
    pass

  # Charge sharing (ratio distribution in local window)
  hMap = dirCluster.Get("clusterShape_ChargeRatio_LocalIndex")
  if (hMap):
    hMap.GetXaxis().SetRangeUser(-5,5)
    hMap.GetYaxis().SetRangeUser(-0.05,1.2)
    hPx = hMap.ProfileX() # TODO: Re-normalized with counts in seed
    hPx.SetLineColor(ROOT.kBlack)
    hPx.SetLineStyle(ROOT.kDashDotted) # dash-dothPx.SetMarkerColor(ROOT.kBlack)
    hPx.SetLineWidth(3)
    self.DrawHist(hMap, "clusterShape_ChargeRatio_LocalIndex", "colz", optNormY=True)
    hPx.Draw("same")
  else:
    pass

  # plot 2D map of charge fractions in pixel
  windowSize = 3.0
  hRatioMean = self.new_obj(ROOT.TH2D(
    f'hChargeSharingRatioMean{suffix}',
    'CE65 - charge sharing by ratio (avg.);column (pixel);row (pixel)',
    int(windowSize), -windowSize/2, windowSize/2,
    int(windowSize), -windowSize/2, windowSize/2))
  hRatioMPV = self.new_obj(ROOT.TH2D(
    f'hChargeSharingRatioMPV{suffix}',
    'CE65 - charge sharing by ratio (MPV);column (pixel);row (pixel)',
    int(windowSize), -windowSize/2, windowSize/2,
    int(windowSize), -windowSize/2, windowSize/2))
  for iy in range(int(windowSize)):
    for ix in range(int(windowSize)):
      index = int(ix + iy * windowSize - (windowSize * windowSize  -1) // 2)
      binx = hMap.GetXaxis().FindBin(index)
      hpfy = hMap.ProjectionY(f'_py_{ix}_{iy}_{suffix}',binx,binx)
      hRatioMean.SetBinContent(ix + 1, iy + 1, hpfy.GetMean())
      peak = hpfy.GetBinCenter(hpfy.GetMaximumBin())
      hRatioMPV.SetBinContent(ix + 1, iy + 1, peak)
      hpfy.Delete()
  self.DrawHist(hRatioMean, 'hChargeSharingRatioMean', 'colz')
  self.draw_hist_text(hRatioMean, color=ROOT.kWhite)
  self.DrawHist(hRatioMPV, 'hChargeSharingRatioMPV', 'colz')
  self.draw_hist_text(hRatioMPV, color=ROOT.kWhite)
    # Cluster shape with highest N/Nth pixels
  hRatio = dirCluster.Get("clusterShape_ChargeRatio_Accumulated")
  hRatio.SetXTitle(f'R_{{n}} (#sum highest N pixels)')
  hRatio.SetYTitle('accumulated charge ratio')
  hRatio.GetXaxis().SetRangeUser(0,10)
  hRatio.GetYaxis().SetRangeUser(0,1.2)
  hPx = hRatio.ProfileX()
  hPx.SetLineColor(ROOT.kBlack)
  hPx.SetLineStyle(ROOT.kDashDotted) # dash-dot
  hPx.SetLineWidth(3)
  hPx.SetMarkerColor(ROOT.kBlack)
  self.DrawHist(hRatio, "Cluster charge ratio", "colz", False, optNormY=True)
  hPx.Draw("same")

  hRatio = dirCluster.Get("clusterShape_ChargeRatio_SortedIndex")
  hRatio.SetXTitle(f'Pixel index (Nth highest charge)')
  hRatio.SetYTitle('#it{q}_{n} charge ratio / #it{Q}_{cluster}')
  hRatio.GetXaxis().SetRangeUser(0,10)
  hRatio.GetYaxis().SetRangeUser(-0.5, 1.5)
  self.DrawHist(hRatio, "Cluster charge ratio", "colz", False, optNormY=True)

  hRatio = dirCluster.Get('clusterShape_Charge_Accumulated')
  hRatio.SetTitle('accumulated charge - Highest N pixels ')
  hRatio.SetYTitle('accumulated charge')
  hRatio.SetXTitle(f'Q_{{n}} (#sum highest N pixels)')
  hRatio.GetXaxis().SetRangeUser(0,10)
  hRatio.GetYaxis().SetRangeUser(0,args.CHARGE_MAX)
  hPx = hRatio.ProfileX()
  hPx.SetLineColor(ROOT.kBlack)
  hPx.SetLineStyle(ROOT.kDashDotted) # dash-dot
  hPx.SetMarkerColor(ROOT.kBlack)
  hPx.SetLineWidth(3)
  self.DrawHist(hRatio, "clusterShape_Charge_Accumulated", "colz")
  hPx.Draw("same")
  # Output
  if(nextPage): self.NextPage()
  return None
CorryPainter.DrawClusteringAnalog = DrawClusteringAnalog

dirTmp = corryHist.Get(clusterModule)
if(dirTmp != None):
  paint.DrawClusteringAnalog(dirTmp.Get(detector))

def DrawCorrelation(self, dirCorr):
  # Init
  self.pageName = f"Correlations"
  detList = [detector] + [f'MIMOSA26_{x}' for x in range(args.nrefs)]
  for detName in detList:
    dirDet = dirCorr.Get(detName)
    if(dirDet == None): continue
    self.NextRow()
    hitmap = dirDet.Get('hitmap_clusters')
    self.DrawHist(hitmap, option='colz', optStat=False)
    if(args.roi and detName != detector):
      xlower, xupper, ylower, yupper = self.select_roi(hitmap, suffix=f'{detName}')
      hitmap_roi = self.new_obj(hitmap.Clone(f'{hitmap.GetName()}_{detName}_roi'))
      hitmap_roi.SetTitle(f'{detName} cluster map with ROI')
      hitmap_roi.GetXaxis().SetRangeUser(xlower, xupper)
      hitmap_roi.GetYaxis().SetRangeUser(ylower, yupper)
      self.DrawHist(hitmap_roi, option='colz', optStat=False)
      corryROI = [[xlower,ylower],[xlower,yupper],[xupper,yupper],[xupper,ylower]]
      print(f'> {detName} roi = {corryROI}')
    self.DrawHist(dirDet.Get('correlationX'), optGaus=True, scale=1000, optStat=True)
    self.DrawHist(dirDet.Get('correlationY'), optGaus=True, scale=1000, optStat=True)
  # Output
  self.NextPage()
  return None
CorryPainter.DrawCorrelation = DrawCorrelation

dirTmp = corryHist.Get(corrModule)
if(dirTmp != None):
  paint.DrawCorrelation(dirTmp)

def DrawTracking4D(self, dirAna):
  # Init
  self.pageName = f"Tracking4D - {args.nrefs} references"
  # Drawing
  h = dirAna.Get("tracksPerEvent")
  h.GetXaxis().SetRangeUser(-0.5,10)
  self.DrawHist(h, "tracksPerEvent", optLogY=True, optStat=True)
  h = dirAna.Get("trackChi2ndof")
  h.GetXaxis().SetRangeUser(0,20)
  self.DrawHist(h, "trackChi2ndof", optLogY=True, optStat=True)
  # Residuals in each plane
  for iRef in range(args.nrefs):
    refName = f'MIMOSA26_{iRef}'
    dirRef = dirAna.Get(refName).Get('global_residuals')
    h = dirRef.Get('GlobalResidualsX')
    h.Rebin(int(0.001 // h.GetBinWidth(1))) # binwidth -> 0.5um
    self.DrawHist(h, 'GlobalResidualsX', optGaus=True, scale=1000, optStat=True)
    h = dirRef.Get('GlobalResidualsY')
    h.Rebin(int(0.001 // h.GetBinWidth(1)))
    self.DrawHist(h, 'GlobalResidualsY', optGaus=True, scale=1000, optStat=True)
  # Interception in DUT
  dirDUT = dirAna.Get(detector)
  if(dirDUT != None):
    self.DrawHist(dirDUT.Get('local_intersect'), option='colz', optStat=False)
  # Output
  self.NextPage()
  return None
CorryPainter.DrawTracking4D = DrawTracking4D

dirTmp = corryHist.Get(trackingModule)
if(dirTmp != None):
  paint.DrawTracking4D(dirTmp)

def DrawDUTAssociation(self, dirAna):
  # Init
  self.pageName = f"DUTAssociation - {detector}"
  # Drawing
  htmp = dirAna.Get('hTrackDUT')
  if not htmp: return
  htmp.GetYaxis().SetRangeUser(-500, 500)
  htmp.GetXaxis().SetRangeUser(-500, 500)
  self.DrawHist(htmp, option='colz', optStat=False)
  htmp = dirAna.Get('hResidualX')
  self.DrawHist(htmp, optGaus=True)
  htmp = dirAna.Get('hResidualY', optStat=True)
  self.DrawHist(htmp, optGaus=True)
  htmp = dirAna.Get('hDistTrackToClusterCentrePos_beforeCut')
  self.DrawHist(htmp, "distance before cut", optStat=True)
  # Output
  self.NextPage()
  return None
CorryPainter.DrawDUTAssociation = DrawDUTAssociation

dirTmp = corryHist.Get(associationModule)
if(dirTmp != None):
  paint.DrawDUTAssociation(dirTmp.Get(detector))

def DrawAlignmentDUT(self, dirAlign):
  # Init
  self.pageName = f"AlignmentDUT - {detector}"
  # Iterations
  grIter = dirAlign.Get(f"alignment_correction_displacementX_{detector}")
  grIter.SetTitle("Alignment correction on displacement - X")
  self.DrawHist(grIter, "alignmentX", optStat=True)
  grIter = dirAlign.Get(f"alignment_correction_displacementY_{detector}")
  grIter.SetTitle("Alignment correction on displacement - Y")
  self.DrawHist(grIter, "alignmentY", optStat=True)
  # Residual X
  hSigX = dirAlign.Get("residualsX")
  hSigX.Rebin(int(1. / hSigX.GetBinWidth(1))) #um
  self.DrawHist(hSigX, "residualsX", optGaus=True, optStat=True)
  # Residual Y
  hSigX = dirAlign.Get("residualsY")
  hSigX.Rebin(int(1. / hSigX.GetBinWidth(1))) #um
  self.DrawHist(hSigX, "residualsX", optGaus=True)
  self.NextPage("AlignmentDUTResidual")
  return None
CorryPainter.DrawAlignmentDUT = DrawAlignmentDUT

dirTmp = corryHist.Get(alignDUTModule)
if(dirTmp != None):
  paint.DrawAlignmentDUT(dirTmp.Get(detector))

def DrawAnalysisDUT(self, dirAna, nextPage=True):
  # Init
  self.pageName = f"AnalysisDUT - {detector}"
  # Summary pad
  hCut = dirAna.Get("hCutHisto")
  self.NextPad()
  nTrack = int(hCut.GetBinContent(1))
  nTrackCutChi2 = int(hCut.GetBinContent(2))
  nTrackCutDUT = int(hCut.GetBinContent(3))
  nTrackCutROI = int(hCut.GetBinContent(4))
  nTrackCutMask = int(hCut.GetBinContent(2))
  nTrackPass = int(hCut.GetBinContent(7))
  nAssociatedCluster = int(hCut.GetBinContent(8))
  # Efficiency stats.
  eff, error, lerr, uerr = efficiency_simple(nAssociatedCluster, nTrackPass)
  pave = self.draw_text(0.15, 0.1, 0.7, 0.9)
  self.add_text(pave, f'Raw efficiency : {eff * 100:.1f}^{{+{uerr * 100:.1f}}}_{{-{lerr * 100:.1f}}} %', font=62, size=0.08)
  self.add_text(pave, f'All tracks N_{{trk}} : {nTrack:.0f}', font=62, size=0.05)
  self.add_text(pave, f'- #chi^{{2}} / Ndf > 1 : -{nTrackCutChi2}')
  self.add_text(pave, f'- outside DUT : -{nTrackCutDUT}')
  self.add_text(pave, f'- outside ROI : -{nTrackCutROI}')
  self.add_text(pave, f'- close to mask : -{nTrackCutMask}')
  self.add_text(pave, f'Track pass selectoin : {nTrackPass}', font=62, size=0.05)
  self.add_text(pave, f'Associated clusters N_{{assoc. cls.}} : {nAssociatedCluster}', font=62, size=0.05)
  pave.Draw()
  # Drawing  
  hMap = dirAna.Get("clusterMapAssoc")
  self.DrawHist(hMap, "clusterSize", "colz", optStat=False)
    # In-eff map (unassociated tracks)
  hMapIneff = dirAna.Get('hUnassociatedTracksLocalPosition')
  nbinx = int(1 // hMapIneff.GetXaxis().GetBinWidth(1))
  nbiny = int(1 // hMapIneff.GetYaxis().GetBinWidth(1))
  hMapIneff.Rebin2D( nbinx , nbiny) # Rebin to 1px
  self.DrawHist(hMapIneff, option='colz', optStat=False)
  # Charge
  self.NextRow()
  hCharge = dirAna.Get('clusterChargeAssociated')
  hCharge.Rebin(int(args.CHARGE_BINWIDTH / hCharge.GetBinWidth(1)))
  hCharge.GetXaxis().SetRangeUser(0,args.CHARGE_MAX)
  self.DrawHist(hCharge, optLangau=True, optStat=True)
  hCharge = dirAna.Get('seedChargeAssociated')
  hCharge.Rebin(int(args.CHARGE_BINWIDTH / hCharge.GetBinWidth(1)))
  hCharge.GetXaxis().SetRangeUser(0,args.CHARGE_MAX)
  self.DrawHist(hCharge, optLangau=True, optStat=True)
  # residualsX
  hSigX = dirAna.Get("global_residuals").Get("residualsX")
  hSigX.Rebin(int(1. / hSigX.GetBinWidth(1)))
  self.DrawHist(hSigX, optGaus=True, optStat=True)
  # residualsY
  hSigX = dirAna.Get("global_residuals").Get("residualsY")
  hSigX.Rebin(int(1. / hSigX.GetBinWidth(1)))
  self.DrawHist(hSigX, optGaus=True, optStat=True)
  
  # Output
  if(nextPage): self.NextPage()
  return None
CorryPainter.DrawAnalysisDUT = DrawAnalysisDUT

dirTmp = corryHist.Get(analysisModule)
if(dirTmp != None):
  paint.DrawAnalysisDUT(dirTmp.Get(detector))

def DrawAnalysisCE65(self, dirAna, nextPage=True):
  # Init
  self.pageName = f"AnalysisCE65"
  # AnalysisDUT
  self.DrawAnalysisDUT(dirAna, nextPage=False)
  # Cluster analysis
  self.NextRow()
  dirCluster = dirAna.Get('cluster')
  self.DrawClusteringAnalog(dirCluster, nextPage=False, suffix='_assoc')
  # Output
  self.pageName = f"AnalysisCE65"
  if(nextPage): self.NextPage()
  return None
CorryPainter.DrawAnalysisCE65 = DrawAnalysisCE65

dirTmp = corryHist.Get("AnalysisCE65")
if(dirTmp != None):
  paint.DrawAnalysisCE65(dirTmp.Get(detector))

paint.PrintBackCover()
corryHist.Close()
