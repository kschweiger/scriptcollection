
#Neue print PDF funktion in plots classe


import ROOT
from rootutils import PDFPrinting


class plots():
    def __init__(self, key):
        self.key = key
        self.Titlestring = "title"
        if key == "Jet_Pt":
            self.setTH1(200,0,600)
            self.Titlestring = "Jet p_{T}"
        elif key == "Jet_corr":
            self.setTH1(100,0.8,1.2)
            self.Titlestring = "Jet jecFactor('Uncorrected')"
        elif key == "Evt_Rho":
            self.setTH1(40,0,60)
            self.Titlestring = "Event #rho"
        elif key == "Jet_Eta":
            self.setTH1(40,-2.4,2.4)
            self.Titlestring = "Jet #eta"
        elif key == "Jet_Mt":
            self.setTH1(200,0,600)
            self.Titlestring = "Jet m_{T}"
        elif key == "Jet_leadTrackPt":
            self.setTH1(100,0,300)
            self.Titlestring = "p_{T} of leading Track in Jet"
        elif key == "Jet_leptonPt":
            self.setTH1(60,0,120)
            self.Titlestring = "p_{T} of Lepton matched to Jet"
        elif key == "Jet_leptonPtRel":
            self.setTH1(30,0,60)
            self.Titlestring = "Rel. p_{T} of Lepton matched to Jet"
        elif key == "Jet_leptonDeltaR":
            self.setTH1(20,0,0.5)
            self.Titlestring = "#Delta R of Lepton matched to Jet"
        elif key == "Jet_leptonPt_all":
            self.setTH1(140,-120,120)
            self.Titlestring = "p_{T} of Lepton matched to Jet"
        elif key == "Jet_nHEFrac" or key == "Jet_nEmEFrac":
            self.setTH1(20,0,1)
            self.Titlestring = key
        elif key == "Jet_chargedMult":
            self.setTH1(35,0,70)
            self.Titlestring = "Charged Multiplicity of Jet"
        elif key == "Jet_vtxPt":
            self.setTH1(100,0,200)
            self.Titlestring = "p_{T} of Vertex"
        elif key == "Jet_vtxMass":
            self.setTH1(14,0,7)
            self.Titlestring = "Mass of Vertex"
        elif key == "Jet_vtx3DVal":
            self.setTH1(30,0,15)
            self.Titlestring = "3D decay length value of Vertex"
        elif key == "Jet_vtxNtracks":
            self.setTH1(13,-0.5,12.5)
            self.Titlestring = "N_{tracks} of Vertex"
        elif key == "Jet_vtx3DSig":
            self.setTH1(150,0,300)
            self.Titlestring = "#sigma of 3D decay length value of Vertex"
        elif key == "Jet_regPt":
            self.setTH1(200,0,600)
            self.Titlestring = "Regressed Jet p_{T}"
        elif key == "Jet_regcorr":
            self.setTH1(96,0.4,1.6)
            self.Titlestring = "p_{T, reg} / p_{T}"
        else:
            print "Key error!",key,"not supported."
            exit()

            
    def setXTitle(self, key, th1f):
        th1f.GetXaxis().SetTitle(self.Titlestring)
        th1f.GetXaxis().SetTitleSize(0.05)
        th1f.GetXaxis().SetTitleOffset(0.75)
        th1f.SetTitle("")
    
    def setYTitle(self, th1f):
        th1f.GetYaxis().SetTitle("arbitrary units")
        th1f.GetYaxis().SetTitleSize(0.05)
        th1f.GetYaxis().SetTitleOffset(0.75)

    def makeSampletext(self,samplestring):
        if samplestring is "ttHbb":
            label = ROOT.TLatex(0.6275,0.908, 'Sample: t#bar{t}H , H #rightarrow b#bar{b}')
        elif samplestring is "ttbar":
            label = ROOT.TLatex(0.77,0.908, 'Sample: t#bar{t}')
        else:
            print "samplesting no supported"
            label = ROOT.TLatex(0.88,0.908, '')
        label.SetTextFont(42)
        label.SetTextSize(0.045)
        label.SetNDC()
        return label    

            
    def makeCMSstuff(self):
        simul = ROOT.TLatex(0.135, 0.908, 'CMS simulation')
        simul.SetTextFont(42)
        simul.SetTextSize(0.045)
        simul.SetNDC()

        cms = ROOT.TLatex(0.135, 0.86, 'work in progress')
        cms.SetTextFont(42)
        cms.SetTextSize(0.045)
        cms.SetNDC()
        
        return simul, cms
        
    def getKey(self):
        return self.key

    def setTH1(self, bins, xmin, xmax):
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax

    def setSumw2(self, th1f):
        th1f.Sumw2()

class CatPlots(plots):    

    def __init__(self, key, cuts, categorizer, legendtext, symmetricCats = True, symmetricColor = True, sample = None):
        plots.__init__(self, key)
        self.samplestring = sample
        if len(cuts) < 3: 
            print "More cuts needed"
            exit()
        self.categorizer = categorizer
        self.legendtext = legendtext
        self.setCatHistos(cuts, symmetricCats, categorizer)
        self.setCatColors(symmetricCats, symmetricColor)
        self.makeLegend(legendtext,symmetricCats, symmetricColor)

        

    def setCatHistos(self, cuts, symmetric, categorizer):
        self.histokeys = []
        self.fullpostfix = []
        if symmetric:
            for postfix in ["neg","pos"]:
                for i in range((len(cuts)-1)/2):
                    self.histokeys.append("histo"+str(i)+postfix+"_"+categorizer)
                    self.fullpostfix.append(str(i)+postfix+"_"+categorizer)
        
        else:
            if self.samplestring is not None:
                postfix = self.samplestring
            else:
                postfix = ""
            for i in range(len(cuts)-1):
                self.histokeys.append("histo"+postfix+str(i)+"_"+categorizer)
                self.fullpostfix.append(postfix+str(i)+"_"+categorizer)

        self.Cathistos = {}
        self.Catlookup = {}
        
        cutindex = 0
        
        for i in range(len(self.fullpostfix)):
            self.Cathistos.update({self.histokeys[i] : ROOT.TH1F(self.key+self.fullpostfix[i],self.key+self.fullpostfix[i], self.bins,self.xmin,self.xmax) })
            self.Catlookup.update({self.histokeys[i] : {"left": cuts[cutindex], "right": cuts[cutindex+1]} })
            cutindex = cutindex + 1

        for key in self.histokeys:
            self.setSumw2(self.Cathistos[key])
            #self.setXTitle(key, self.Cathistos[key])

    def setCatColors(self, symmetricCats, symmetricColors):
        nhistos = len(self.fullpostfix)
        colorlist = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
        colorlist_asym = [ROOT.kGreen+2, ROOT.kBlue+2, ROOT.kRed+2]
        colorlist_add = [ROOT.kViolet, ROOT.kYellow,ROOT.kOrange, ROOT.kAzure, ROOT.kPink+10]
        self.CatColors = {}
        if symmetricCats:
            if symmetricColors:
                if nhistos == 12:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue+1,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen-1,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+1,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+1,ROOT.kRed+2]
                if nhistos == 10:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue+1,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+1,ROOT.kRed+2]
                if nhistos == 8:
                    colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kGreen-2,ROOT.kGreen,ROOT.kGreen,ROOT.kGreen+2,ROOT.kRed,ROOT.kRed+2]
            else:
                print nhistos
                colorlist = colorlist + colorlist_asym
            for i, key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })
        else:
            print nhistos
            if nhistos == 7:
                colorlist = [ROOT.kBlue+2,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed+2]
                colorlist = colorlist[::-1]
            elif nhistos == 5:
                colorlist = [ROOT.kBlue+2,ROOT.kAzure-4,ROOT.kGreen,ROOT.kOrange-4,ROOT.kRed+2]
                colorlist = colorlist[::-1]
            elif nhistos == 11:
                colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen-3,ROOT.kGreen,ROOT.kGreen+2,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2]
                colorlist[::-1]
            elif nhistos == 9:
                colorlist = [ROOT.kBlue+2,ROOT.kBlue,ROOT.kAzure-4,ROOT.kTeal+5,ROOT.kGreen,ROOT.kYellow-9,ROOT.kOrange-4,ROOT.kRed,ROOT.kRed+2]
                colorlist[::-1]
            else:
                colorlist = [ROOT.kViolet+7,ROOT.kViolet+6,ROOT.kViolet+1,ROOT.kViolet,ROOT.kViolet-4,ROOT.kViolet-8,ROOT.kMagenta+1,ROOT.kMagenta-10]
            for i,key in enumerate(self.histokeys):
                self.CatColors.update({ key : colorlist[i] })

    def FillCatHistos(self, fillval, catval):
        for key in self.histokeys:
            if catval >= self.Catlookup[key]["left"] and catval < self.Catlookup[key]["right"]:
                self.Cathistos[key].Fill(fillval)
                break
    
    def makeStyle(self):
        for key in self.histokeys:
            self.Cathistos[key].SetLineColor(ROOT.kBlack) #set Color
            self.Cathistos[key].SetFillStyle(1001)
            self.Cathistos[key].SetFillColor(self.CatColors[key]) #set Color

    def makeStack(self,order = "<"):
            
        self.makeStyle()
        self.Stackplot = ROOT.THStack("Stack"+self.key,"Stack "+self.key)

        
        
        #for i in range(len(self.histokeys)/2):
        #    print self.histokeys[i], self.histokeys[(len(self.histokeys)-1)-i]
         #   self.Stackplot.Add(self.Cathistos[self.histokeys[i]])            
          #  self.Stackplot.Add(self.Cathistos[self.histokeys[(len(self.histokeys)-1)-i]])
        tmplist = []
        for key in self.Cathistos:
            tmplist.append(self.Catlookup[key]["left"])
        tmplist = sorted(tmplist)
        if order == "<":
            tmplist = tmplist #tmplist is orderd from left to right category
        elif order == ">":
            tmplist = tmplist[::-1] #turn tmplist -> ordered from right to left category
        else:
            print "ordering unknown!"
            exit()
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.Stackplot.Add(self.Cathistos[key])            
                    break
        #self.setXTitle(self.key,self.Stackplot)

    def DrawStack(self):
        self.Stackplot.Draw()
        self.leg.Draw("same")
        raw_input("press  Ret")

    def WriteStack(self, canvas, pdfout = None):
        #self.Stackplot.Write()
        self.Stackplot.Draw("histoe")
        self.setXTitle(self.key,self.Stackplot)
        self.leg.Draw("same")
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.samplestring is not None:
            label = self.makeSampletext(self.samplestring)
            label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)

    def makeLegend(self, categorizer, symmetricCats, symmetricColor):
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            self.leg = ROOT.TLegend(0.13,0.55,0.43,0.83)
        else:
            self.leg = ROOT.TLegend(0.6,0.55,0.88,0.88)
        self.leg.SetBorderSize(0)
        self.leg.SetTextFont(42)
        self.leg.SetFillStyle(0)
        tmplist = []
        for key in self.Cathistos:
            tmplist.append(self.Catlookup[key]["left"])
        tmplist = sorted(tmplist)
        for element in tmplist:
            for key in self.Cathistos:
                if element == self.Catlookup[key]["left"]:
                    self.leg.AddEntry(self.Cathistos[key],str(self.Catlookup[key]["left"])+" <= "+categorizer+" < "+str(self.Catlookup[key]["right"]))
                    break


class normPlots(plots):
    def __init__(self, key, comparison = False, nComparisons = 2, legendtext = []):
        plots.__init__(self, key)
        if comparison:
            self.nHistos = nComparisons
        else:
            self.nHistos = 1
        self.legendtext = legendtext
        if comparison:
            self.histos = []
            for i in range(nComparisons):
                self.histos.append(ROOT.TH1F(self.key+"_"+str(i),self.key+"_"+str(i), self.bins,self.xmin,self.xmax))
        else:
            self.histos = [ROOT.TH1F(self.key,self.key, self.bins,self.xmin,self.xmax)]
        for histo in self.histos:
            self.setSumw2(histo)


    
    def makeStyle(self, maxyval, dofilling = False):
        colorlist = [ROOT.kBlue, ROOT.kViolet-3,ROOT.kGreen+3,ROOT.kTeal-6]
        self.setXTitle(self.key,self.histos[0])
        self.setYTitle(self.histos[0])
        self.histos[0].GetYaxis().SetRangeUser(0,maxyval*1.1)
        for iHisto, histo in enumerate(self.histos):
            histo.SetLineWidth(2)
            histo.SetLineColor(colorlist[iHisto])
            if dofilling:
                histo.SetFillStyle(1001)
                histo.SetFillColor(ROOT.kCyan-10)

    def makeLegend(self, legendtext):
        if len(legendtext) != self.nHistos:
            if self.nHistos != 1:
                print "Generating generic Legendtext"
            legendtext = []
            for i in range(self.nHistos):
                legendtext.append(self.key+" "+str(i))
        specialpos = ["Jet_regcorr","Jet_corr"]
        if self.getKey() in specialpos:
            leg = ROOT.TLegend(0.13,0.70,0.43,0.83)
        else:
            leg = ROOT.TLegend(0.6,0.70,0.88,0.88)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.SetFillStyle(0)
        for ihisto, histo in enumerate(self.histos):
            print "adding", legendtext[ihisto]
            leg.AddEntry(histo, legendtext[ihisto])
        return leg

    def FillnormHisto(self,fillval,nHisto = 0):
        self.histos[nHisto].Fill(fillval)
        
    def WriteHisto(self, canvas, samplestring = None, dofilling = False, Drawnormalized = False, pdfout = None):
        if Drawnormalized:
            for histo in self.histos:
                ScaletoInt(histo)
        maxy = 0
        for histo in self.histos:
            tmpval = histo.GetBinContent(histo.GetMaximumBin())
            if tmpval > maxy:
                maxy = tmpval
        self.makeStyle(maxy, dofilling)
        legend = self.makeLegend(self.legendtext)
        stuff = "histoe"
        for histo in self.histos:
            print stuff
            histo.Draw(stuff)
            if not stuff.endswith("same"):
                stuff = stuff + " same"
        canvas.Update()
        simul, cms = self.makeCMSstuff()
        simul.Draw("same")
        cms.Draw("same")
        if self.nHistos > 1:
            print "drawing legend"
            legend.Draw("same")
        else:
            label = self.makeSampletext(samplestring)
            label.Draw("same")
        canvas.SetTitle(self.key)
        canvas.SetName(self.key)
        canvas.Update()
        canvas.Write()
        if pdfout is not None:
            pdfout.addCanvastoPDF(canvas)
        

def ScaletoInt(th1f):
    th1f.Scale(1/float(th1f.Integral()))


