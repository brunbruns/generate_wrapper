import os
from generate_wrapper import *

print("\n\n*********************** Wrapper Generator ***********************\n***************************************************************** \n")

top_path = "/home/t0264060/stage_cocotb_2022/library_perso/generate_wrapper/hdl_basic_demo/mul.vhd" #enter here the vhdl top on which wrapper will be generated 
wrapper_path= "/home/t0264060/stage_cocotb_2022/library_perso/generate_wrapper/hdl_basic_demo/wrapped_mul.vhd" #enter here the path, with name where the wrapper should be generated
clk_name="clk" #the name of the clk port is declared here 

edit_shell=0
if edit_shell == 1: #change value to enable to enter paths in shell, either path can be changed in the code  
    #ask value to user
    entry=input(f"\ttop_path is {top_path} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        if os.path.exists(entry):
            top_path = entry
        else: #check the validity of the path
            print("***ERROR: unvalid path")
            quit() 
    entry=input(f"\twrapper_path is {wrapper_path} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        wrapper_path = entry
    entry=input(f"\tclock port name on top is {clk_name} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        clk_name = entry

wrap(wrapper_path, top_path , clk_name)