# nk2-FL(mixer)
Hello folks, I have now also written a program for the Korg nanoKontrol2 (nK2) with which the mixer (possibly more later) can be operated.

<b>Changes in Version 1.2</b>
* Version 1.2 is more performant and button conflict has been resolved.
* own Korg Kontrol Editor-Mappinge-File: FL Studio - nK2_Knob1-8.nktrl2_data
  copy it to ..\FL-Studio\System\Hardware specific\Korg nanoKONTROL 2\
  Load it in Korg Kontrol Editor and write Data to nanoKontrol2-device Communication\Write Scene Data
* You can control the Master-MixerTrack (Id=0)
* testing.py is no longer available.

The program assigns the 8 control groups of the nK2, each matching mixer tracks. This means that the Solo button switches the assigned mixer track to solo [on / off].
Mute = mute, Rec = Arm disk recording. The rotary knob controls the panning, the slide control the volume.
When the script is started, the first 8 mixer tracks are assigned. With the [Track Rew / Track FF] the selected mixer tracks are shifted 8 positions left / right,
With [Marker Rew / Marker FF] ​​you can move the selected area step by step. With [set] you can set the step size, default values ​​[1,2,4,10,16,20,25,50], but you can change them. The 8 controlled mixer tracks are identified by a name prefix, ("[1] =", "[2] =", "[3] =", "[4] =", "[5] =", " [6] = "," [7] = "," [8]).
When leaving the area, these name changes are removed again and marked the next 8. When exiting the script, all name changes made by the program should be removed. If you want to do this manually, you can do this with the [cycle] button. This removes all name prefixes ("[1] =", "[2] =", "[3] =", "[4] =", "[5] =", "[6] =", "[ 7] = "," [8]).
The selected MixerTracks are also displayed as HintMsg and are notified of the reaching of the beginning / end of the MixerTracks.

With the transport button: [Rew, FF, Stop, Play, Rec] the corresponding playlist functions are switched [on / off].

The script consists of 5 files. The actual device file "<b>device_Mixer Control.py</b>" contains the corresponding function and action calls and must be copied into the corresponding FL script directory "... \ Image-Line \ Data \ FL Studio \ Settings \ Hardware \ Korg nanoKontrol ", the script name is" # name = nanoKontrol2 - Mixer V1.2 (Lonz) "
This is the script that you have to assign to the nanoKntrol2 in the midi settings. In the subdirectory nK2 ("... \ Image-Line \ Data \ FL Studio \ Settings \ Hardware \ Korg nanoKontrol \ nK2") there are further files.

<b>nK2_Classes.py</b>: Emulates the nanoKontrol2 (class TNK_Control: ...) and its elements as software classes. This should make it easier for me to address the various buttons when programming.

<b>nK2_FL.py</b>: Generates an instance (NK_FL) of class TNK_Control, with the values ​​of the "Korg Kontrol Editor - FL Studio - nanoKontrol2_nktrl2_data".
	And there is a problem here. The Track Rew button has CC-No = 0 and values ​​64/63 for off / on, Track FF has CC-No = 0 and values ​​64/65 for off / on. The first knob for panning also has CC-Nr = 0 (that's stupid) and the value range 0-127. If this controller is now in the range 63-65, the program cannot decide which button has actually been pressed and operating errors may occur if you change the buttons at that very moment. You can solve the problem by pressing another button.
	In another version of Scrip, I want to work with my own Korg Kontrol Editor - mapping file to eliminate the problem. Then you need the mapping file or the settings for the script.
	
<b>userPara.py</b>: Contains a few parameters that you can change.
	Flag_No_Sel_Names = False: If you set this value to True, the scrip does not generate a name prefix ("[1] =", "[2] =", "[3] =", "[4] =", "[5] = "," [6] = "," [7] = "," [8]).
		If you prefer.
	Reg_Snap = False / True: If the range of the MixerTracks to be controlled is shifted, the positions of the controls (panning and volume) of the nK2 probably do not match the 	position of the MixerTrack in FL Studio. 
		With Reg_Snap = True, the controller only takes effect when it is close to the FL Studio value and you avoid jumps in value.
		However, you may also regulate in void. With Reg_Snap = False, FL Studio immediately follows the controller.
		There may be jumps, but you have direct control. (I prefer False).
	lsSPT_Values ​​= [1,2,4,10,16,20,25,50]: These are the step sizes that can be set with [set]. You can choose these as long as the Python List syntax is correct.
		Some examples are given in userPara.py. Only one list should be active at a time. Please comment out all others with #.

<b>FL Studio - nK2_Knob1-8.nktrl2_data</b>: Mapping-File for Korg Kontrol Editor

In addition, the subdirectory ... \ info contains other files that have nothing to do with the script but are intended to serve as information.
	Info_ger.txt \ Info_eng.txt this file in German or English
	FL Studio - nanoKontrol2_nktrl2_data.txt 						Values ​​of the mapping file, as text
	Korg Kontrol Editor - FL Studio - nK2_Knob1-8.nktrl2_data.png	Values ​​of the mapping file, as an image
