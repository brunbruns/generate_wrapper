



def wrap(wrapper_path, top_path , clk_name):
    #file declarationa and opening 
    
    wrapper_name= wrapper_path.split("/")[-1]#will be use for wrapper generation   
    wrapper_name= wrapper_name.split(".")[0] #supress .vhd

    top_name= top_path.split("/")[-1]#will be use for wrapper generation   
    top_name= top_name.split(".")[0] #supress .vhd
    


    port =[] #list of string with port name 
    direction =[] #list of string with port direction
    type =[] #list of string with port type
    identify_component= False #boolean to knwo if compent as been found
    identify_end = False #boolean to know that all port have been found 
    try:
        file_r = open(top_path, 'r') #open in read mode (no need to change) 
    except:
        return("error top path is invalid")

    ################### read the file to identify port
    
    while not identify_component or not identify_end:
        line = file_r.readline()
        
        if not line:##in case of file is read till the end and programme failed 
            
            break#end of while 
        line = line.lower() #VHDL doesn't have a specific case sensitivity 
        
        if not identify_component : #look for component declaration  
            if line.find ("entity") != -1 and line.find("is") != -1: #line for entity declaration should be :   entity <entity_name> is
                identify_component = True 
                line = line[line.find ("entity"): line.find("is")] # troncate in case their is other char on the line (comment)
                line = line.replace("entity","") #replace is better than strip, strip only remove at start and end of a str 
                line = line.replace(" ","") #remove spaces  
                entity_name=line #name of the entity 
                
        
        elif identify_component: #if component is identified, look for port 
            
            if (line.find("end") != -1 and line.find(entity_name) != -1) == 1:  #look for "end" and entity name on the same line (separated in case of multiple space or tab)
                identify_end = True #stop the reading loop  

                type[-1]=type[-1][:-1]#supress last char which was a ')' closing entity declaration  
                
            
            elif line.find(":") != -1: #according to "standard" writing name of port should be before those :
                
                line = line.split(":")
                
                #find port name
                line0=line[0] 
                if line0.find("signal") != -1 : # if end sequence isn't detected signal could be seen as port, however if port name contain signal only a warning is displayed 
                    print("**Warning: line with signal keyword take as a port**")
                line0=line0.replace('port','')
                line0=line0.replace('(','')
                line0=line0.replace(' ','')
                port.append(line0)
                # find direction
                if line[1].find("in") != -1:
                    direction.append("in")
                else:
                    direction.append("out")
                #find type
                line=line[1]  
                line=line[:line.find(";")]#stop line at ; (case of comment) 
                line=line.replace("in","")
                line=line.replace("out","")
                line=line.strip()# dont use replace remove space cause downto need spaces, here only remove at start and end
                type.append(line)
    
    #end of reading process
    
    file_r.close()

    #verify that clock port and clk_name are the same
    check_clk_name=0
    for k in range(len(port)):
        if port[k]==clk_name:
            check_clk_name = 1
    
    if check_clk_name == 0 :
        return (f"error clock port {clk_name} not found ")

     
    ### here declaration of usefull string, could be stored in a json but still storing in the very own python code isn't a bad practice here
    str_import="library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n\n" 
    str_clk="\n\ncomponent clock is\n\tPort ( clk : out STD_LOGIC);\nend component;\n"
    str_clk_pm="\nbegin\n\tclkpm: clock port map (clk => s_clk);\n\n" #here on a single line  



    #################################### generate vhdl wrapper  

    if identify_component and identify_end:#only generate wrapper if source file was read with sucess 
        
        try:
            file_w= open(wrapper_path, 'w') #here write mode needed (also overwrite in case file existe)  
        except:
            return("error wrapper path is invalid")
        file_w.write(str_import)
        
        file_w.write("entity "+wrapper_name +  " is\n")
        file_w.write("\tPort(\n")
        for k in range(len(port)):#delclaration of entity 
            if port[k]!=clk_name: #clk port has to be removed at the top of the wrapper 
                
                if k< len(port)-1:
                    file_w.write( "\t\t" + port[k]+ " : " + direction[k] + " " + type[k]+ ";\n"   )
                else:
                    file_w.write( "\t\t" + port[-1]+ " : " + direction[-1] + " " + type[-1]+ ");\n"   ) #last line is different 
        file_w.write("end "+wrapper_name+";\n")

        file_w.write("architecture struct of "+wrapper_name+" is")
        file_w.write(str_clk) #declaration of clk component  
        #declaration of component which is wrapped 
        file_w.write("\n\ncomponent "+top_name +  " is\n")
        file_w.write("\tPort(\n")
        for k in range(len(port)):#delclaration of entity 

            if k< len(port)-1:
                file_w.write( "\t\t" + port[k]+ " : " + direction[k] + " " + type[k]+ ";\n"   )
            else:
                file_w.write( "\t\t" + port[-1]+ " : " + direction[-1] + " " + type[-1]+ ");\n"   ) #last line is different 
        file_w.write("end component;\n")
        
        file_w.write("\nsignal s_clk: std_logic;--signal s_clk is declared to offer acces on it from cocotb easily as dut.s_clk\n")
        
        file_w.write(str_clk_pm) #write clk port map 
        
        file_w.write("\ttoppm: "+ top_name + " port map(\n")
        for k in range(len(port)):#delclaration of entity 
            if port[k] == clk_name: #clk port has to be removed at the top of the wrapper 
                if k< len(port)-1:
                    file_w.write( "\t\t" + port[k] + "=>"+ " " + port[k]+ ",\n"   )
                else:
                    file_w.write( "\t\t" + port[k] + "=>"+ " " + port[k]+ ");\n"   ) #last line is different 
            else: #case where the port is the clk, here connect at s_clk
                if k< len(port)-1:
                    file_w.write( "\t\t" + port[k] + "=>"+ " " + "s_clk"+ ",\n"   )
                else:
                    file_w.write( "\t\t" + port[k] + "=>"+ " " + "s_clk"+ ");\n"   ) #last line is different
        file_w.write("\n\nend struct;")  
        file_w.close()
        
        ports=""
        for k in range(len(port)):
            ports=ports+port[k]+"  "

        return(f"wrapper generated: {len(port)} ports identified\n"+ports)
    
    else:
        if not identify_component:
            return("error entity declaration not found during top reading")
        if not identify_end:
            return("error entity end marker not found during top reading")
    print("\n*****************************************************************")

    
