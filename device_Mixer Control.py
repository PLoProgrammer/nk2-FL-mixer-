# name=nanoKontrol2 - Mixer V1 (Lonz)
# url=https://forum.image-line.com/viewtopic.php?p=1483607#p1483607


import transport
import mixer
import ui
import midi
import time
from nK2.nK2_FL import *
from nK2.userPara import *

Tog_TP=True #toggel TP-Button rewind and fastforward
Tog_OMM=True #toggel OnMidiMsg / not in use

lsChan = [20,30,40,50,60,70,80,90] #idx-Channel-Zuweisungen
lsKnob = [21,31,41,51,61,71,81,91] #idx-Knobs
lsSld = [22,32,42,52,62,72,82,92] #idx-Slider
lsSoloB = [23,33,43,53,63,73,83,93] #idx-Solo-Button
lsMuteB = [24,34,44,54,64,74,84,94] #idx-Mute-Button
lsRecB = [25,35,45,55,65,75,85,95] #idx-Rec-Button
lsSelTrackNames = ["[1]= ","[2]= ","[3]= ","[4]= ","[5]= ","[6]= ","[7]= ","[8]= "] #Name addition for selected tracks. Will be added at the front
ST_HintMsg=1.0 #Time to show Hint-Msg
FL_TR_COUNT_MAX=125 #max numbers of Mixer-Tracks

NK_CC_SLider_First = 36 # CC-Number first Slider
NK_CC_Slider_Last = 43 # CC-Number Slider 8 (last)
NK_CC_Knob_First = 0 # CC-Number first Knob
NK_CC_Knob_Last = 7 # CC-Number Knob 8 (last)
NK_Solo_But_First = 0 # CC-Number first Slider
NK_Solo_But_Last = 7 # CC-Number Slider 8 (last)
NK_Mute_But_First = 36 # CC-Number first Slider
NK_Mute_But_Last = 43 # CC-Number Slider 8 (last)
NK_Rec_But_First = 72 # CC-Number first Slider
NK_Rec_But_Last = 79 # CC-Number Slider 8 (last)

MT_LastNr = 0
StepsPerTick=1
#lsSPT_Values is defined in nK2.userPara.py.
SPT_IDX=0#Index for lsSPT_Values
Tog_Steps=True #toggel Step-Ticker between Up(+1) and Down(-1) 
goTo=0

#Helper function
def beep():
	print__func("beep()")
	pass
		
#Selection function in FL-Mixer

def selectActivMixTrack(MixTrackNr):
	print__func("selectActivMixTrack("+str(MixTrackNr)+")")
#Select only MixTrackNr
	mixer.setTrackNumber(MixTrackNr,1)
		
def selectActivArea(goTo):
	print__func("selectActivArea("+str(goTo)+")")
#mark the 8 tracks that are controlled
	if Flag_No_Sel_Names: return
	x=NK_NrOf_ControlGr+1#9
	if goTo+NK_NrOf_ControlGr>FL_TR_COUNT_MAX:
		goL_Delta=(goTo+NK_NrOf_ControlGr-FL_TR_COUNT_MAX)
		x=x-goL_Delta
		#goTo=goTo-goL_Delta
	for i in range(goTo+1,goTo+x):
		orgName= mixer.getTrackName(i)
		mixer.setTrackNumber(i,1)
		if isSelName(orgName)==False: mixer.setTrackName(i,lsSelTrackNames[i-goTo-1]+orgName[0:])
		
#reset selection function
def isSelName(lastName):
	print__func("isSelName("+lastName+")")
#check is it my SelectionName
	if lastName[0]=='[' and lastName[2]==']': return True
	else: return False

#reset last selction Tracknames (namePrefix)
def resetTrackName(event,lastIdx):
	print__func("resetTrackName("+str(event)+", "+str(lastIdx)+")")
	if Flag_No_Sel_Names: return
	for i in range(lastIdx,lastIdx+8):
		lastName= mixer.getTrackName(i+1)
		if isSelName(lastName): mixer.setTrackName(i+1,lastName[5:])
	
#reset all Track-namePrefix
def resetAllName():
	print__func("resetAllName()")	
	if Flag_No_Sel_Names: return
	ui.setHintMsg("reset namePrefix")
	time.sleep(ST_HintMsg)
	for i in range(0,FL_TR_COUNT_MAX+1):
		lastName= mixer.getTrackName(i)
		if isSelName(lastName): mixer.setTrackName(i,lastName[5:])



#Main class NK-Control	
class TNKaction():
#Script/NK-Control: given function =========
	def OnInit(self):
		print__func("TNKaction.OnInit()")	
		#resetAllName()
		goTo=0
		selectActivArea(goTo)	
		Tog_TP=True
		Tog_OMM=True
		Tog_Steps=True
		StepsPerTick=1

	def OnDeInit(self):
		print__func("TNKaction.OnDeInit()")	
		resetAllName()
		
	def OnMidiIn(self, event):
		print__func("TNKaction.OnMidiIn("+str(event)+")")
		pass
		
	def OnMidiMsg(self, event):
		print__func("TNKaction.OnMidiMsg("+str(event)+")")
		global Tog_OMM
		FoundButton=[False,"",0,0,0]	#[Gefunden?,Name,idx,event.data1,event.data2]
		FoundButton = getButton(event, FoundButton)
		if FoundButton[0]: self.actionButton(event, FoundButton)
		#if "NK_R" in FoundButton[1]: print("Regler")



# my NK-Control-function =========
	def actionButton(self, event, FoundButton):	
		print__func("TNKaction.actionButton("+str(event)+", "+str(FoundButton)+")")
	#Action to Button (wiht my Index FoundButton[2])
		global goTo
		global Tog_TP
		global Tog_Steps
		global StepsPerTick
		global lsSPT_Values
		global SPT_IDX
		snapVal=7
		
		def goRight(steps):
			print__func("TNKaction.actionButton.goRight("+str(steps)+")")
		#Selection go steps to the rigeht sight of Mixer
			sEnd=" "
			global goTo #Warum hier global und in goSteps nicht?
			lastgoTo=goTo
			if goTo+NK_NrOf_ControlGr+steps < FL_TR_COUNT_MAX: goTo=goTo+steps #print("right")
			else: 
				goTo=FL_TR_COUNT_MAX-NK_NrOf_ControlGr
				sEnd="END of Mixer (right)! - "	#wird mir goTo nie überschritten
				beep()
			sHi_MixTR_Range=sEnd+"Mix-Tracks "+str(1+goTo)+"-"+str(NK_NrOf_ControlGr+goTo) #activ HintMsg Track area
			ui.setHintMsg(sHi_MixTR_Range)
			if lastgoTo!=goTo: resetTrackName(event,lastgoTo)
			selectActivArea(goTo)
			event.handled = True

		def goLeft(steps):
			print__func("TNKaction.actionButton.goLeft("+str(steps)+")")
			#Selection go steps to the left sight of Mixer
			sEnd=" "
			global goTo 
			lastgoTo=goTo
			if goTo > steps-1: goTo=goTo-steps #print("left")
			else: 
				goTo=0
				sEnd="END of Mixer (left)! - "
				beep()
			sHi_MixTR_Range=sEnd+"Mix-Tracks "+str(1+goTo)+"-"+str(NK_NrOf_ControlGr+goTo) #activ HintMsg Track area
			ui.setHintMsg(sHi_MixTR_Range)
			if lastgoTo!=goTo: resetTrackName(event,lastgoTo)
			selectActivArea(goTo)

		if FoundButton[2]==2: #8 to left
			print__action("move 8 step left "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			goLeft(NK_NrOf_ControlGr)
			
		elif FoundButton[2]==3: #8 to right 
			print__action("move 8 step right "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			goRight(NK_NrOf_ControlGr)
			
		elif FoundButton[2]==4: #reset
			print__action("Cycle "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			resetAllName()
			event.handled = True #sonst knallt es
			
		elif FoundButton[2]==5: #set stepswide
		### Könnte ich dazu verwenden um einen Track fest zu zu ordnen
			if Tog_Steps and SPT_IDX<len(lsSPT_Values): 
				SPT_IDX+=1
				if SPT_IDX==(len(lsSPT_Values)-1): Tog_Steps = not Tog_Steps#max 7 per Ticker, Toggel betwenn Up/down
			elif SPT_IDX>0:
				SPT_IDX-=1
				if SPT_IDX==0: Tog_Steps = not Tog_Steps#max 7 per Ticker
			else: print("Error: Step-Counter")
			StepsPerTick=lsSPT_Values[SPT_IDX]
			ui.setHintMsg("set "+str(lsSPT_Values[SPT_IDX])+" steps")
			print__action("set "+str(lsSPT_Values[SPT_IDX])+" steps")
			event.handled = True
			time.sleep(ST_HintMsg)
			
		elif FoundButton[2]==6: #StepsPerTick) to left
			print__action("move "+str(StepsPerTick)+" step left "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			goLeft(StepsPerTick)

		elif FoundButton[2]==7: #StepsPerTick) to right
			print__action("move "+str(StepsPerTick)+" step right "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			goRight(StepsPerTick)
			
		elif FoundButton[2]==8: #TP Rew
			print__action("TP Rew "+FoundButton[1]+" Wert: "+str(FoundButton[4]))
			if Tog_TP: transport.rewind(2)
			else: transport.rewind(0)
			Tog_TP= not Tog_TP
			event.handled = True
			
		elif FoundButton[2]==9: #TP FF
			print__action("TP FF "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			if Tog_TP: transport.fastForward(2)
			else: transport.fastForward(0)
			Tog_TP= not Tog_TP
			event.handled = True
			
		elif FoundButton[2]==10: #TP stop 
			print__action("TP stop "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			if Tog_TP: transport.fastForward(2)
			transport.stop()
			event.handled = True
			
		elif FoundButton[2]==11: #TP play
			print__action("TP play "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			transport.start()
			event.handled = True
			
		elif FoundButton[2]==12: #TP rec
			if bPrintAction: print("TP rec ",FoundButton[1]," Wert: ",FoundButton[4])
			print__action("TP rec "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			transport.record()
			event.handled = True
			
		elif FoundButton[2] in lsKnob: #Paning
			print__action("Knob "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			nMixTrIndex=FoundButton[3]-(NK_CC_Knob_First-1) #36to43-35=MixTrackIdx in FL
			nMixTrPan=(1/64)*(FoundButton[4]-63) # max Pan. FL=-1.0 - 1.0 (0-127 steps)
			FL_Pan=int(mixer.getTrackPan(nMixTrIndex+goTo)*64)
			#print("Pan. nK2: ",FoundButton[4]-63," FL: ",(mixer.getTrackPan(nMixTrIndex+goTo)))
			
			#Only change the value if the position of the controller matches the FL value. To avoid jumps
			if FoundButton[4]-63 in range(FL_Pan-snapVal,FL_Pan+snapVal) and Reg_Snap: 	mixer.setTrackPan(nMixTrIndex+goTo, nMixTrPan) #Set Paning
			if Reg_Snap==False: mixer.setTrackPan(nMixTrIndex+goTo, nMixTrPan) #Set Paning
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True

		elif FoundButton[2] in lsSld: #Volume
			print__action("Slider "+FoundButton[1]+" Wert: "+str(FoundButton[4]))			
			nMixTrIndex=FoundButton[3]-(NK_CC_SLider_First-1) #36to43-35=MixTrackIdx in FL
			nMixTrVolu=(1/127)*FoundButton[4] # max Vol. FL=1.0 / max Vol. nK2=127, event.data2=Value from nK2-Slider
			#print("Vol. nK2: ",FoundButton[4]," FL: ",(mixer.getTrackVolume(nMixTrIndex+goTo)*127))
			FL_Vol=int(mixer.getTrackVolume(nMixTrIndex+goTo)*127)
			#Only change the value if the position of the controller matches the FL value. To avoid jumps
			if FoundButton[4] in range(FL_Vol-snapVal,FL_Vol+snapVal) and Reg_Snap: mixer.setTrackVolume(nMixTrIndex+goTo, nMixTrVolu) #Set Vol
			if Reg_Snap==False: mixer.setTrackVolume(nMixTrIndex+goTo, nMixTrVolu) #Set Vol
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True
		
		elif FoundButton[2] in lsSoloB: #Solo-Button
			nMixTrIndex=FoundButton[3]+1 #+1 in FL
			print__action("Solo Button "+FoundButton[1]+" Idx: "+str(nMixTrIndex)+"+"+str(goTo)+" Wert: "+str(FoundButton[4]))			
			selectActivMixTrack(nMixTrIndex+goTo)
			mixer.soloTrack(nMixTrIndex+goTo) #
			event.handled = True
			
		elif FoundButton[2] in lsMuteB: #Mute-Button
			nMixTrIndex=FoundButton[3]-(NK_Mute_But_First-1) #36to43-35=MixTrackIdx in FL
			print__action("Mute Button "+FoundButton[1]+" Idx: "+str(nMixTrIndex)+"+"+str(goTo)+" Wert: "+str(FoundButton[4]))			
			mixer.muteTrack(nMixTrIndex+goTo) #
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True

		elif FoundButton[2] in lsRecB: #Rec-Button
			nMixTrIndex=FoundButton[3]-(NK_Rec_But_First-1) #72to73-71=MixTrackIdx in FL
			print__action("Rec Button "+FoundButton[1]+" Idx: "+str(nMixTrIndex)+"+"+str(goTo)+" Wert: "+str(FoundButton[4]))			
			mixer.armTrack(nMixTrIndex+goTo) #
			selectActivMixTrack(nMixTrIndex+goTo)
			event.handled = True
	
		
TNKaction = TNKaction()


def OnInit():
	ui.showWindow(midi.widMixer)
	TNKaction.OnInit()

def OnDeInit():
	TNKaction.OnDeInit()

def OnMidiIn(event):
	TNKaction.OnMidiIn(event)

def OnMidiMsg(event):
	TNKaction.OnMidiMsg(event)

