# Parameter user can change
# after changing this file must be saved and the script reloaded

#To identify the 8 mixer tracks that are currently controlled by the nK2-Contoler, 
#the track names are prefixed with ("[1] =", "[2] =", "[3] =", "[4] = "," [5] = "," [6] = "," [7] = "," [8] = "). If the area is left, the prefixes are removed.
#Who does NOT want this can set the flag to True.
Flag_No_Sel_Names=False #Set the flag True if the selected array should not be marked with special names
#with the [cycle] -Button you can reset all prefixed

Reg_Snap = False #True = controllers only take effect if they are close to the FL value (no value jumps), False = controllers take effect directly, possibly value jumps 
#If you move the 8 mixer array, the position Slider \ Knob may not correspond to the value in FL and jumps occur

#With the [set] button you can switch between different step sizes.
#You can change the individual step sizes and the length of the list.
#With set, the list is first run through from left to right and, when reaching the end, from right to left.
#
#other possible examples 
#only one list can be active at a time, all others must be commented out with the #
#======== Lists
lsSPT_Values = [1,2,4,10,16,20,25,50] #possible Values for StepsPerTick
#lsSPT_Values = [1,2,3,4,5,6,7] 
#lsSPT_Values = [1,2]
#lsSPT_Values = [1,2,10,20]
#lsSPT_Values = [1,50,125] #go to end or start
#lsSPT_Values = [your list ...] 
