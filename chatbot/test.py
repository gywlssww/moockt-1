def chkTime(mystr):
    if len(mystr)==0:
        return "e"
    mystr = mystr.strip()
    lastchar = mystr[-1]
    print(lastchar)
    print(mystr[:-1])
    if lastchar == '분':
        if len(mystr[:-1])>0 and mystr[:-1].isdigit():
            sft_time = int(mystr[:-1])*60
        else:
            sft_time = "e"            
    elif lastchar == '초':
        if len(mystr[:-1])>0 and mystr[:-1].isdigit():
            sft_time = int(mystr[:-1])
        else:
            sft_time = "e"
    elif lastchar == '뒤' or lastchar == '후':
        mystr = mystr[:-1].strip()
        sft_time = str(chkTime(mystr))+"+"
        
    elif lastchar == '전':
        mystr = mystr[:-1].strip()
        sft_time = str(chkTime(mystr))+"-"
    return str(sft_time)

return_str = "2초 뒤"
sft_time = chkTime(return_str)
print(sft_time)