import os
from generate_wrapper import *
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile


#note to execute with python3 to have tk
 
print("\n\n*********************** Wrapper Generator ***********************\n***************************************************************** \n")

top_path = "/home/t0264060/stage_cocotb_2022/library_perso/generate_wrapper/hdl/mul.vhd" #enter here the vhdl top on which wrapper will be generated 
wrapper_path= "/home/t0264060/stage_cocotb_2022/library_perso/generate_wrapper/hdl/wrapped_mul.vhd" #enter here the path, with name where the wrapper should be generated
clk_name="clk" #the name of the clk port is declared here 

edit_shell=3
if edit_shell == 0:  #execute with value harcoded here
    wrap(wrapper_path, top_path , clk_name)
elif edit_shell == 1: #change value to enable to enter paths in shell, either path can be changed in the code  
    #ask value to user
    entry=input(f"\ttop_path is {top_path} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        top_path = entry
        
    entry=input(f"\twrapper_path is {wrapper_path} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        wrapper_path = entry
    entry=input(f"\tclock port name on top is {clk_name} type a new or press enter\n-->")
    if entry != "": #keep the default value if no entry 
        clk_name = entry
    print("launching function:\n")
    print("***********************")
    print(wrap(wrapper_path, top_path , clk_name))

else : #in other case open a GUI 

    # create root window
    root = Tk()
    root.geometry('1000x320')
    w=1000#define width and heigth 
    h=320

    # root window title and dimension
    root.resizable(False, False)
    root.title("VHDL Wrapper Generator GUI")

    # all widgets will be here
    #first create button to launch wrapper generator  
    def wrap_onClick():
        #on click the 2 path are read and clk
        top_path=edit_top_path.get(1.0, 'end') 
        wrapper_path=edit_wrapper_path.get(1.0, 'end')
        clk_name = edit_clk_name.get(1.0, 'end')
        top_path= top_path.replace('\n','') #remove enter 
        wrapper_path= wrapper_path.replace('\n','')
        clk_name = clk_name.replace('\n','')
        #launch fun 
        result= wrap(wrapper_path, top_path , clk_name)
        label_result.config(text = result)  #display result 
        if result.find("error") != -1:
           #if error set text in red 
            label_result.config(fg = 'red')
        else: 
            label_result.config(fg = 'blue') #case were thing went wrong first         
    button = Button(root, text='Generate',command=wrap_onClick).place(x=0.815*w, y=0.85*h)

    box_width= 120
    #create an editText for top_path
    label_top_instruction = Label(root, text='Enter the top path here')
    label_top_instruction.place(x=0.03*w, y=0.09*h)
    edit_top_path = Text(root, height=1, width=box_width)
    edit_top_path .place(x=0.05*w, y=0.15*h)
    edit_top_path.config(bg='white')
    #create botton for file explorer for top path
    def topFile():
        file = askopenfile(mode ='r', filetypes =[('VHDL file', '*.vhd')]) 
        edit_top_path.delete(1.0,"end")
        edit_top_path.insert(1.0, file.name)
    buttonTop = Button(root, text='open',width= 5,command=topFile).place(x=0.92*w, y=0.14*h)
    #create an editText for wrapper_path
    label_wrapper_instruction = Label(root, text='Enter a path for the wrapper here')
    label_wrapper_instruction.place(x=0.03*w, y=0.29*h)
    edit_wrapper_path = Text(root, height=1, width=box_width)
    edit_wrapper_path .place(x=0.05*w, y=0.35*h)
    edit_wrapper_path.config(bg='white')
    #create botton for file explorer for wrapper path
    def wrapFile():
        file = asksaveasfile(mode ='w', filetypes =[('VHDL file', '*.vhd')]) 
        edit_wrapper_path.delete(1.0,"end")
        edit_wrapper_path.insert(1.0, file.name)
    buttonWrapper = Button(root, text='save as',command=wrapFile, width= 5).place(x=0.92*w, y=0.34*h)
    #clock name
    label_wrapper_instruction = Label(root, text='Enter the top clock port name here')
    label_wrapper_instruction.place(x=0.03*w, y=0.49*h)
    edit_clk_name = Text(root, height=1, width=box_width)
    edit_clk_name.place(x=0.05*w, y=0.55*h)
    edit_clk_name.config(bg='white') 
    #label for result 
    label_result = Label(root, text='')
    label_result.place(x=0.03*w, y=0.70*h)
    label_result.config(fg = 'blue')
    
     


    # Execute Tkinter
    root.mainloop()