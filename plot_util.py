#!/bin/env python3

# Utility lib for corryvreckan plot

# Based on pyROOT
import ROOT
from ROOT import TMath
  # Colors
from ROOT import kBlack, kRed, kBlue, kGreen, kViolet, kCyan, kOrange, kPink, kYellow, kMagenta, kGray, kWhite
  # Markers
from ROOT import kFullCircle, kFullSquare, kOpenCircle, kOpenSquare, kOpenDiamond, kOpenCross, kFullCross, kFullDiamond, kFullStar, kOpenStar, kOpenCircle, kOpenSquare, kOpenTriangleUp, kOpenTriangleDown, kOpenStar, kOpenDiamond, kOpenCross, kOpenThreeTriangles, kOpenFourTrianglesX, kOpenDoubleDiamond, kOpenFourTrianglesPlus, kOpenCrossX, kFullTriangleUp, kOpenTriangleUp, kFullCrossX, kOpenCrossX, kFullTriangleDown, kFullThreeTriangles, kOpenThreeTriangles, kFullFourTrianglesX, kFullDoubleDiamond, kFullFourTrianglesPlus
  # Lines
from ROOT import kSolid, kDashed, kDotted, kDashDotted
  # Objects
from ROOT import TCanvas, TPaveText
from ROOT import gPad, gStyle

import sys, os, datetime, math, json, logging
from array import array

# From ALICE collaboration editor guidelines
def ALICEStyle(graypalette = False):
  print("[-] INFO - Setting ALICE figure style")
  ROOT.gStyle.Reset("Plain")
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetOptStat(0)
  if(graypalette):
    ROOT.gStyle.SetPalette(8,0)
  else:
    ROOT.gStyle.SetPalette(1)
  ROOT.gStyle.SetCanvasColor(10)
  ROOT.gStyle.SetCanvasBorderMode(0)
  ROOT.gStyle.SetFrameLineWidth(1)
  ROOT.gStyle.SetFrameFillColor(kWhite)
  ROOT.gStyle.SetPadColor(10)
  ROOT.gStyle.SetPadTickX(1)
  ROOT.gStyle.SetPadTickY(1)
  ROOT.gStyle.SetPadTopMargin(0.02)
  ROOT.gStyle.SetPadBottomMargin(0.12)
  ROOT.gStyle.SetPadLeftMargin(0.14)
  ROOT.gStyle.SetPadRightMargin(0.02)
  ROOT.gStyle.SetHistLineWidth(1)
  ROOT.gStyle.SetHistLineColor(kRed)
  ROOT.gStyle.SetFuncWidth(2)
  ROOT.gStyle.SetFuncColor(kGreen+3)
  ROOT.gStyle.SetLineWidth(2)
  ROOT.gStyle.SetLabelSize(0.045,"xyz")
  ROOT.gStyle.SetLabelOffset(0.01,"y")
  ROOT.gStyle.SetLabelOffset(0.01,"x")
  ROOT.gStyle.SetLabelColor(kBlack,"xyz")
  ROOT.gStyle.SetTitleSize(0.05,"xyz")
  ROOT.gStyle.SetTitleOffset(1.2,"y")
  ROOT.gStyle.SetTitleOffset(1.1,"x")
  ROOT.gStyle.SetTitleFillColor(kWhite)
  ROOT.gStyle.SetTextSizePixels(26)
  ROOT.gStyle.SetTextFont(42)
  ROOT.gStyle.SetLegendBorderSize(0)
  ROOT.gStyle.SetLegendFillColor(kWhite)
  ROOT.gStyle.SetLegendFont(42)

def InitALICELabel(x1 = 0.02, y1 = 0.03, x2 = 0.35, y2 = 0.1, size=0.04, align=13, type="perf", pos='lt'):
  """Draw text relative to pad edges
  
  Position:
    x1 - Label pave to near edge X
    x2 - Label pave to away edge X
    y1 - Label pave to near edge Y
    y2 - Label pave to away edge Y
  """
  PAD_EDGE_LEFT = ROOT.gPad.GetLeftMargin()
  PAD_EDGE_RIGHT = 1 - ROOT.gPad.GetRightMargin()
  PAD_EDGE_BOTTOM   = ROOT.gPad.GetBottomMargin()
  PAD_EDGE_TOP   = 1 - ROOT.gPad.GetTopMargin()
  if pos == 'lt': # Left Top
    xlower = PAD_EDGE_LEFT + x1
    xupper = PAD_EDGE_LEFT + x2
    ylower = PAD_EDGE_TOP - y2
    yupper = PAD_EDGE_TOP - y1
  elif pos == 'rt':
    xlower = PAD_EDGE_RIGHT - x2
    xupper = PAD_EDGE_RIGHT - x1
    ylower = PAD_EDGE_TOP + y1
    yupper = PAD_EDGE_TOP + y2
  elif pos == 'lb':
    xlower = PAD_EDGE_LEFT + x1
    xupper = PAD_EDGE_LEFT + x2
    ylower = PAD_EDGE_BOTTOM + y1
    yupper = PAD_EDGE_BOTTOM + y2
  elif pos == 'rb':
    xlower = PAD_EDGE_RIGHT - x2
    xupper = PAD_EDGE_RIGHT - x1
    ylower = PAD_EDGE_BOTTOM + y1
    yupper = PAD_EDGE_BOTTOM + y2
  else:
    xlower, ylower, xupper, yupper = x1, y1, x2, y2
  pTxtALICE = ROOT.TPaveText(xlower, ylower, xupper, yupper,"brNDC")
  pTxtALICE.SetBorderSize(0)
  pTxtALICE.SetFillColor(0)
  pTxtALICE.SetFillStyle(0)
  pTxtALICE.SetTextSize(size)
  pTxtALICE.SetTextFont(42) # Helvetica
  pTxtALICE.SetTextAlign(align) # Top Left
  if(type == "perf"):
    text = "ALICE Performance"
  elif(type == "simul"):
    text = "ALICE Simulation"
  elif(type == "prel"):
    text = "ALICE Preliminary"
  else:
    text = type
  txt = pTxtALICE.AddText(text)
  txt.SetTextFont(42) # Helvetica Bold
  return pTxtALICE

# Select color and marker style in pre-defined group
  # Use Bool isNEW to reset the index
COLOR_SET_DEFAULT = [kBlack, kRed, kBlue, kGreen+3, kOrange, kViolet, kCyan, kOrange-6, kPink]
COLOR_SET_ALICE = [kBlack, kRed+1 , kBlue+1, kGreen+3, kMagenta+1, kOrange-1,kCyan+2,kYellow+2]
COLOR_SET_ALICE_FILL = [kGray+1,  kRed-10, kBlue-9, kGreen-8, kMagenta-9, kOrange-9,kCyan-8,kYellow-7] # For systematic bands
COLOR_SET = COLOR_SET_DEFAULT
COLOR_INDEX = -1
def SelectColor(COLOR_INDEX = -1):
  while(COLOR_INDEX < 100):
    yield COLOR_SET[COLOR_INDEX % len(COLOR_SET)]
    COLOR_INDEX += 1

# Marker Style
kRound,  kBlock, kDelta, kNabla, kPenta, kDiamond, kCross, kClover, kClover4, kStar, kIronCross, kXMark = 20, 21, 22, 23, 29, 33, 34, 39, 41, 43, 45, 47
kRoundHollow, kBlockHollow, kDeltaHollow, kNablaHollow, kPentaHollow, kDiamondHollow, kCrossHollow, kCloverHollow, kClover4Hollow, kStarHollow, kIronCrossHollow, kXMarkHollow = 24, 25, 26, 32, 30, 27, 28, 37, 40, 42, 44, 46
MARKER_SET_DEFAULT = [kFullCircle, kOpenSquare, kCross, kFullTriangleUp, kOpenDiamond, kFullStar, kFullSquare, kOpenCross, kFullDiamond, kFullCrossX]
MARKER_SET_ALICE = [kFullCircle, kFullSquare, kOpenCircle, kOpenSquare, kOpenDiamond, kOpenCross, kFullCross, kFullDiamond, kFullStar, kOpenStar]
DATA_MARKER = [kFullCircle, kFullSquare, kFullTriangleUp, kFullTriangleDown, kFullStar, kFullDiamond, kFullCross, kFullThreeTriangles, kFullFourTrianglesX, kFullDoubleDiamond, kFullFourTrianglesPlus, kFullCrossX]
MC_MARKER = [kOpenCircle, kOpenSquare, kOpenTriangleUp, kOpenTriangleDown, kOpenStar, kOpenDiamond, kOpenCross, kOpenThreeTriangles, kOpenFourTrianglesX, kOpenDoubleDiamond, kOpenFourTrianglesPlus, kOpenCrossX]
MARKER_SET = MARKER_SET_DEFAULT
MARKER_INDEX = -1
def SelectMarker(MARKER_INDEX = 0):
  while(MARKER_INDEX < 100):
    yield MARKER_SET[MARKER_INDEX % len(MARKER_SET)]
    MARKER_INDEX += 1
COLOR = SelectColor()
MARKER = SelectMarker()
# Line Style
LINE_STYLE_SET = [kSolid, kDashed, kDotted, kDashDotted]
LINE_STYLE_INDEX = -1
def SelectLine(LINE_STYLE_INDEX = 0):
  while(LINE_STYLE_INDEX < 100):
    yield LINE_STYLE_SET[LINE_STYLE_INDEX % len(LINE_STYLE_SET)]
    LINE_STYLE_INDEX += 1
LINE = SelectLine()

# Fit
def fcn_moyal(x : list, par : list):
  """Moyal Distribution
  Approximation for Landau distribution
  Reference:

  Parameter
    par[0]=mean
    par[1]=sigma
  """
  mean = par[0]
  sigma = par[1]
  t = (x[0] - mean) / sigma
  invsq2pi = 0.3989422804014
  expPseudo = -0.5 * (TMath.Exp(-t) + t)
  return invsq2pi / sigma * (TMath.Exp( expPseudo ))
  
def fcn_langaus(x : list, par : list):
  """Convoluted Landau and Gaussian Fitting Function

  Reference: https://root.cern/doc/master/langaus_8C.html

  Parameter
    par[0]=Width (scale) parameter of Landau density
    par[1]=Most Probable (MP, location) parameter of Landau density
    par[2]=Total area (integral -inf to inf, normalization constant)
    par[3]=Width (sigma) of convoluted Gaussian function
  """
  invsq2pi = 0.3989422804014  # (2 pi)^(-1/2)
  mpshift  = -0.22278298   # Landau maximum location
  np = 100.0 # number of convolution steps
  sc =   5.0 # convolution extends to +-sc Gaussian sigmas
  xx, mpc, fland, sum = 0., 0., 0., 0.
  xlow, xupp, step = 0., 0., 0.
  x[0] = x[0]
  for i in range(4):
    par[i] = par[i]
  mpc = par[1] - mpshift * par[0]
  xlow = x[0] - sc * par[3]
  xupp = x[0] + sc * par[3]
  step = (xupp-xlow) / np
  # Convolution integral of Landau and Gaussian by sum
  for i in range(1,int(np//2+1)):
    xx = xlow + (i - .5) * step
    fland = TMath.Landau(xx, mpc, par[0]) / par[0]
    sum += fland * TMath.Gaus(x[0], xx, par[3])
    xx = xupp - (i-.5) * step
    fland = TMath.Landau(xx, mpc, par[0]) / par[0]
    sum += fland * TMath.Gaus(x[0], xx, par[3])
  return float(par[2] * step * sum * invsq2pi / par[3])

# Painter
def NewCanvas(name="c1_painter", title="New Canvas", winX=1600, winY=1000, **kwargs):
  return TCanvas(name, title, winX,winY)

class Painter:
  """Master of ROOT drawing and plotting
  Output stored in PDF file
  
  Parameters:
    Canvas - name, title, winX, winY, nx, ny
    Gausssian - gausFitRange
  """
  def __init__(self, canvas = None, printer = "out.pdf", **kwargs):
    self.canvas = canvas if canvas is not None else NewCanvas(**kwargs)
       # Output PDF in 1 file
    self.printer = printer if printer.endswith(".pdf") else printer +".pdf"
    self.printAll = kwargs.get('printAll', False)
    self.printDir = kwargs.get('printDir', os.path.dirname(self.printer))
    if(self.printDir == ''): self.printDir = '.'
    self.printExt = kwargs.get('printExt', ['pdf','png'])
    self.saveROOT = kwargs.get('saveROOT', False)
    if self.saveROOT:
      self.rootfile = ROOT.TFile(printer.replace('.pdf','.root'), 'RECREATE')
    # Configuration
    self.subPadNX = kwargs.get('nx', 1)
    self.subPadNY = kwargs.get('ny', 1)
    0.14, 0.02, 0.12, 0.02
    self.marginTop = kwargs.get('marginTop', 0.02)
    self.marginBottom = kwargs.get('marginBottom', 0.12)
    self.marginLeft = kwargs.get('marginLeft', 0.14)
    self.marginRight = kwargs.get('marginRight', 0.02)
    self.showGrid = kwargs.get('showGrid', False)
    self.gridColor = kwargs.get('gridColor', kGray+1)
    ROOT.gStyle.SetGridColor(self.gridColor)
    self.showPageNo = kwargs.get('showPageNo', False)
    # Parameters
    self.GAUS_FIT_RANGE = kwargs['gausFitRange'] if kwargs.get('gausFitRange') else 1 # ratio of FWHM
    # Status
    self.padIndex = 0
    self.pageNo = 0
    self.pageName = "Start"
    self.padEmpty = True
    self.hasCover = False
    self.hasBackCover = False
    self.primaryHist = None
    self.counterSavedObjs = 0
    # Dump
    self.root_objs = []         # Temp storage to avoid GC
  def __del__(self):
    if(self.hasCover and not self.hasBackCover):
      self.PrintBackCover('')
    if self.saveROOT:
      self.rootfile.Close()
      print('[-] ROOT objects saved to ' + self.rootfile.GetName())
      print(f'> save_obj & TObject.Write() calls - {self.counterSavedObjs}')
  def save_obj(self, obj): # ROOT.TObject
    if not self.saveROOT: return
    self.rootfile.cd()
    if type(obj) is list:
      for tobj in obj:
        tobj.Write()
        self.counterSavedObjs += 1
    else:
      obj.Write()
      self.counterSavedObjs += 1
  def new_obj(self, obj):
    self.root_objs.append(obj)
    return self.root_objs[-1]
  def new_legend(self, xlow, ylow, xup, yup):
    lgd = self.new_obj(ROOT.TLegend(xlow, ylow, xup, yup))
    return lgd
  def add_text(self, pave : ROOT.TPaveText, s : str, **textAttr):
    text = pave.AddText(s)
    textAttr['color'] = textAttr.get('color', kBlack)
    textAttr['size'] = textAttr.get('size', 0.04)
    textAttr['font'] = textAttr.get('font', 42)
    textAttr['align'] = textAttr.get('align', 11)
    text.SetTextAlign(textAttr['align'])
    text.SetTextSize(textAttr['size'])
    text.SetTextFont(textAttr['font'])
    text.SetTextColor(textAttr['color'])
    return text
  def draw_text(self, xlow=0.25, ylow=0.4, xup=0.75, yup=0.6, title = '', **textAttr):
    pave = self.new_obj(ROOT.TPaveText(xlow, ylow, xup, yup, "brNDC"))
    pave.SetBorderSize(0)
    pave.SetFillStyle(0) # hollow
    pave.SetFillColor(ROOT.kWhite)
    if(title != ''):
      # Text Attributes
      textAttr['color'] = textAttr.get('color', kBlack)
      textAttr['size'] = textAttr.get('size', 0.05)
      textAttr['font'] = textAttr.get('font', 62)
      textAttr['align'] = textAttr.get('align', 11)
      self.add_text(pave, title, **textAttr)
    return pave
  def ResetCanvas(self):
    self.canvas.Clear()
    if(self.subPadNX * self.subPadNY > 1):
      self.canvas.Divide(self.subPadNX, self.subPadNY)
    self.padEmpty = True
    # Style
    ROOT.gPad.SetMargin(self.marginLeft, self.marginRight, self.marginBottom, self.marginTop)
    ROOT.gPad.SetGrid(self.showGrid, self.showGrid)
  def SetLayout(self, nx, ny):
    self.subPadNX = nx
    self.subPadNY = ny
    self.ResetCanvas()
  def GetLayout(self):
    return (self.subPadNX, self.subPadNY)
  def draw_pageno(self):
    # Left-Bottom corner
    self.draw_text(0.01,0.01,0.05,0.05,f'{self.pageNo}', 
      size=0.03, color=kGray+1, align=12).Draw()
  def PrintCover(self, title = '', isBack = False):
    self.canvas.Clear()
    pTxt = ROOT.TPaveText(0.25,0.4,0.75,0.6, "brNDC")
    if(title == ''):
      if(isBack):
        pTxt.AddText('Thanks for your attention!')
      else:
        pTxt.AddText(self.canvas.GetTitle())
    else:
      pTxt.AddText(title)
    self.canvas.cd()
    self.canvas.Draw()
    pTxt.Draw()
    if(isBack):
      self.canvas.Print(self.printer + ')', 'Title:End')
    else:
      self.draw_pageno()
      text_footnote = {
        'align': 32,
        'color': kGray+1,
        'size': 0.03,
      }
      pave = self.draw_text(0.5, 0, 1.0, 0.15, f'File : {self.printer}', **text_footnote)
      self.add_text(pave, f'Timestamp : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', **text_footnote)
      self.add_text(pave, f'Powered by #bf{{root_plot}}', **text_footnote)
      pave.Draw()
      self.canvas.Print(self.printer + '(', 'Title:Cover')
    pTxt.Delete()
    self.ResetCanvas()
  def PrintBackCover(self, title=''):
    self.PrintCover(title, isBack=True)
  def NextPage(self, title=""):
    # Print
    if self.printAll and not self.padEmpty:
      figureName = title
      if title == '':
        figureName = f'{self.primaryHist.GetName()}_{len(self.root_objs)}'
      figurePath = f'{self.printDir}/{figureName}'
      for ext in self.printExt:
        self.canvas.SaveAs(figurePath + '.' + ext)
    if(title == ""):
      title = self.pageName
    self.pageNo += 1
    if(self.showPageNo):
      self.canvas.cd()
      self.draw_pageno()
    self.canvas.Print(self.printer, f"Title:{title}")
    # New page
    self.padIndex = 0
    self.ResetCanvas()
  def NextPad(self, title=""):
    # Full sub-pads
    if(self.padIndex == self.subPadNX * self.subPadNY):
      self.NextPage()
    self.padIndex = self.padIndex + 1
    self.canvas.cd(self.padIndex)
    self.padEmpty = True
    self.primaryHist = None
    # Style
    ROOT.gPad.SetMargin(self.marginLeft, self.marginRight, self.marginBottom, self.marginTop)
    ROOT.gPad.SetGrid(self.showGrid, self.showGrid)
  def NextRow(self):
    while(self.padIndex % self.subPadNX != 0):
      self.NextPad()
  # Painter Objects
  def draw_band(self, xmin, xmax, color = kGray+1, style=3002, **kwargs):
    """Draw a rectangular band by TGraph
    Default: vertical gray band crossing the frame
    """
    grshade = self.new_obj(ROOT.TGraph(4))
    ROOT.gPad.Update()
    ymin = kwargs.get('ymin', ROOT.gPad.GetUymin())
    ymax = kwargs.get('ymax', ROOT.gPad.GetUymax())
    grshade.SetPoint(0, xmin, ymax)
    grshade.SetPoint(1, xmax, ymax)
    grshade.SetPoint(2, xmax, ymin)
    grshade.SetPoint(3, xmin, ymin)
    grshade.SetFillColor(color)
    grshade.SetFillStyle(style)
    grshade.SetLineColor(0)
    grshade.SetLineWidth(0)
    grshade.SetMarkerColor(0)
    grshade.SetMarkerSize(0)
    grshade.SetDrawOption('F')
    grshade.Draw('same F')
    return grshade
  # Drawing - Histograms
  def set_hist_palette(self, hist : ROOT.TH2, width=0.05):
    palette = hist.GetListOfFunctions().FindObject("palette")
    totalWidth = width + 0.05 + 0.05 # palette, label, title
    # Pad
    ROOT.gPad.SetRightMargin(totalWidth + self.marginRight)
    # Palette
    palette.SetX1NDC(1. - totalWidth)
    palette.SetX2NDC(1. - totalWidth + width)
    palette.SetY1NDC(self.marginBottom)
    palette.SetY2NDC(1. - self.marginTop)
    return palette
  def hist_rebin(self, hist, binning):
    """binning: width, min, max
    """
    binwidth = binning[0]
    valmin = binning[1]
    valmax = binning[2]
    nbingroup = int ( binwidth // hist.GetBinWidth(1))
    hist.Rebin(nbingroup)
    hist.GetXaxis().SetRangeUser(valmin, valmax)
  def new_hist(self, name, title, binning):
    """binning: width, min, max
    """
    binwidth = binning[0]
    valmin = binning[1]
    valmax = binning[2]
    nbins = int( (valmax - valmin) // binwidth)
    return self.new_obj(ROOT.TH1F(name, title, nbins, valmin, valmax))
  def draw_hist_text(self, hist, **textAttr):
    """Plot bin content as text for ROOT.TH2
    """
    xlower = ROOT.gPad.GetLeftMargin()
    xupper = 1 - ROOT.gPad.GetRightMargin()
    ylower = ROOT.gPad.GetBottomMargin()
    yupper = 1 - ROOT.gPad.GetTopMargin()
    wx = (xupper - xlower) / hist.GetNbinsX()
    wy = (yupper - ylower) / hist.GetNbinsY()
    # Text attributes
    textAttr['color'] = textAttr.get('color', kBlack)
    textAttr['size'] = textAttr.get('size', 0.06)
    textAttr['font'] = textAttr.get('font', 62)
    textAttr['align'] = textAttr.get('color', 22)
    for iy in range(hist.GetNbinsY()):
      for ix in range(hist.GetNbinsX()):
        val = hist.GetBinContent(ix + 1, iy +1)
        pave = self.draw_text(ix * wx + xlower, iy * wy + ylower, (ix+1) * wx + xlower, (iy+1)*wx + xlower)
        self.add_text(pave,f'{val:.3f}', **textAttr)
        pave.Draw('same')
  # Calculation
  def normalise_profile_y(self, hist):
    for ix in range(1,hist.GetNbinsX()+1):
      hpfx = hist.ProjectionY(f'_py_{ix}', ix, ix)
      norm = hpfx.GetMaximum()
      if norm < 1: continue
      for iy in range(1,hist.GetNbinsY()+1):
        raw = hist.GetBinContent(ix, iy)
        hist.SetBinContent(ix, iy, 1. * raw / norm)
      hpfx.Delete()
    return None
  def estimate_fwhm(self, hist):
    """Calculate FWHM and center for TH1D
    """
    peak = hist.GetMaximum()
    rms = hist.GetRMS()
    mean = hist.GetMean()
    halfLeft = hist.FindFirstBinAbove(peak/2.)
    halfRight = hist.FindLastBinAbove(peak/2.)
    center = 0.5 * (hist.GetBinCenter(halfRight) + hist.GetBinCenter(halfLeft))
    fwhm = hist.GetBinCenter(halfRight) - hist.GetBinCenter(halfLeft)
    if fwhm < 2 * hist.GetBinWidth(1):
      print(f'[X] Warning  - Histogram {hist.GetName()} - FWHM too narrow {center = :.2e}, {fwhm = :.2e}, {rms = :.2e}, {peak = :.2e}')
      return rms, mean
    return fwhm, center
  # Fitting -> Fitter?
  def optimise_hist_langau(self, hist, scale=1, **kwargs):
    """Adaptive fitter for Landau-Gaussian distribution
    """
    # Parameters
    N_PARS = 4
    fwhm, center = self.estimate_fwhm(hist)
    fitRange = kwargs.get('fitRange')
    if(not fitRange): fitRange = [0.3*hist.GetMean(), 1.5*hist.GetMean()]
    area = hist.Integral()
    pars = [
      [fwhm * 0.1, fwhm * 0., fwhm * 1],
      [center, center * 0.5, center * 2],
      [10 * area, area * 5, area * 100],
      [fwhm * 0.1, fwhm * 0., fwhm * 1],
    ]
    # Fitter
    langaufun = None
    try:
      langaufun = getattr(ROOT, 'langaufun')
    except AttributeError:
      script_path = os.path.dirname( os.path.realpath(__file__) )
      macroPath = script_path + '/langaus.C'
      if os.path.exists(macroPath):
        # C macro, faster than python implementation
        ROOT.gInterpreter.ProcessLine(f'#include "{macroPath}"')
        langaufun = ROOT.langaufun
      else:
        # python internel implementation
        langaufun = fcn_langaus
    fcnName = f'fitLangaus_{hist.GetName()}_{len(self.root_objs)}'
    fcnfit = self.new_obj(ROOT.TF1(fcnName, langaufun, fitRange[0], fitRange[1], N_PARS))
    startvals = [par[0] for par in pars]
    parlimitslo = [par[1] for par in pars]
    parlimitshi = [par[2] for par in pars]
    fcnfit.SetParameters(array('d', startvals))
    fcnfit.SetParNames("Width","MP","Area","GSigma")
    for i in range(N_PARS):
      fcnfit.SetParLimits(i, parlimitslo[i], parlimitshi[i])
    resultPtr = hist.Fit(fcnName, 'RB0SQN')
    try:
      params = resultPtr.GetParams()
    except ReferenceError:
      self.draw_text(0.50, 0.55, 0.80, 0.85, 'Langau fitting FAILED').Draw('same')
      print(f'[X] Warning  - {hist.GetName()} - Langau fitting FAILED')
      return None
    fiterrs = array('d',[0.] * N_PARS)
    fiterrs = fcnfit.GetParErrors()
    # Draw
    fcnfit.SetRange(hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    if(kwargs.get('color')):
      fcnfit.SetLineColor(kwargs['color'])
    if(kwargs.get('style')):
      fcnfit.SetLineStyle(kwargs['style'])
    if(kwargs.get('width')):
      fcnfit.SetLineWidth(kwargs['width'])
    fcnfit.Draw('lsame')
    if(kwargs.get('notext')):
      return fcnfit, resultPtr
    pave = self.draw_text(0.58, 0.55, 0.85, 0.85,title='Landau-Gaussian')
    self.add_text(pave, f'#chi^{{2}} / NDF = {resultPtr.Chi2():.1f} / {resultPtr.Ndf()}')
    self.add_text(pave, f'Mean = {hist.GetMean():.2e}')
    for ipar in range(N_PARS):
      self.add_text(pave, f'{fcnfit.GetParName(ipar)} = {params[ipar]:.2e}')
    pave.Draw('same')
    return fcnfit, resultPtr
  def optimise_hist_gaus(self, hist, scale=1, **kwargs):
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
    fitRange = min(5 * rms, self.GAUS_FIT_RANGE * fwhm)
    fcnGaus = self.new_obj(
      ROOT.TF1(f'fcnFitGaus_{hist.GetName()}_{len(self.root_objs)}',
      'gaus', center - fitRange, center + fitRange))
    resultPtr = hist.Fit(fcnGaus,'SQN','', center - fitRange, center + fitRange)
    try:
      params = resultPtr.GetParams()
    except ReferenceError:
      print(f'[X] Warning  - Fitting failed with {center = }, {fwhm = }, {rms = }, {peak = }')
      return None
    mean = params[1]
    sigma = params[2]
    fcnGaus.SetRange(mean - 5 * sigma, mean + 5 * sigma)
    fcnGaus.Draw('same')
    drawRange = min(15 * rms, 10 * params[2])
    hist.GetXaxis().SetRangeUser(center - drawRange, center + drawRange)
    if(kwargs.get('color')):
      fcnGaus.SetLineColor(kwargs['color'])
    if(kwargs.get('style')):
      fcnGaus.SetLineStyle(kwargs['style'])
    if(kwargs.get('width')):
      fcnGaus.SetLineWidth(kwargs['width'])
    fcnGaus.Draw('lsame')
    if(kwargs.get('notext')):
      return fcnGaus, resultPtr
    # Draw info
    pave = self.new_obj(ROOT.TPaveText(0.18, 0.55, 0.45, 0.85,'NDC'))
    pave.SetFillColor(ROOT.kWhite)
    self.add_text(pave, f'mean (#mu) = {params[1] * scale:.1f}')
    self.add_text(pave, f'#sigma = {params[2] * scale:.1f}')
    self.add_text(pave, f'#chi^{{2}} / NDF = {resultPtr.Chi2():.1f} / {resultPtr.Ndf()}')
    self.add_text(pave, f'RMS = {rms * scale:.1f}')
    self.add_text(pave, f'FWHM = {fwhm * scale:.1f}')
    pave.Draw('same')
    return resultPtr
  def DrawHist(self, htmp, title="", option="", optStat=False, samePad=False, optGaus=False, scale=1, **kwargs):
    # ROOT.gStyle.SetOptStat(optStat)
    if optStat:
      ROOT.gStyle.SetOptStat(1101)
    else:
      pass
    if(title == ""):
      title = htmp.GetTitle()
    if(not samePad):
      self.NextPad(title)
    elif not self.padEmpty:
      option = f'{option}same'
    else:
      self.primaryHist = htmp
    print("[+] DEBUG - Pad " + str(self.padIndex) + ' : ' + htmp.GetName())
    if kwargs.get('optNormY') == True:
      self.normalise_profile_y(htmp)
    htmp.Draw(option)
    self.padEmpty = False
    # Style
    if(option == "colz"):
      zmax = htmp.GetBinContent(htmp.GetMaximumBin())
      htmp.GetZaxis().SetRangeUser(0.0 * zmax, 1.1 * zmax)
    if(htmp.ClassName().startswith('TH') and self.subPadNX * self.subPadNY >= 4):
      htmp.SetTitleSize(0.08, "XY")
      htmp.SetTitleOffset(0.8, "XY")
    if(optGaus): self.optimise_hist_gaus(htmp, scale)
    if(kwargs.get('optLangau') == True):
      self.optimise_hist_langau(htmp, scale)
    ROOT.gPad.SetLogx(kwargs.get('optLogX') == True)
    ROOT.gPad.SetLogy(kwargs.get('optLogY') == True)
    ROOT.gPad.SetLogz(kwargs.get('optLogZ') == True)


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