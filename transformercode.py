import re
import sys
block_num = 0
BLOCKS = ('if', 'for')
code = """
x=50
if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  elif x > 30:
    print("and also above 30!")
  else:
    print("but not above 30.")
elif x < 5:
  print("below 5")    
"""

def fix_elif_error(line, varName):
        new_string = f'{line.replace("elif", f"if {varName} != 1 and")}'
        return new_string

def replace_keyword_in_block(main_block_orig_lines, level):
    varName = f'valid{str(level)}'
    i = 0
    for line in (main_block_orig_lines):
        if 'elif' in line:
            main_block_orig_lines[i] = fix_elif_error(line, varName)
        if 'if' in line and level == len(line) - len(line.lstrip()):
            main_block_orig_lines[i] += f"{' ' * (level+4)}{varName} = 1\n" 
        i += 1
    return main_block_orig_lines



def process_blocks(lines, level):
    main_block_orig_lines = [] #All original lines at current level
    main_block_processed_lines = [] #All processed lines at current level
    global block_num
    sub_block_orig_lines = []
    
    new_sub_block = False #No new sub-blocks initially
    sub_block_level = None
    for line in lines:
        match = re.search("\w+", line)  #find the first "word" in the line 
        indent_level = 0 
        #line = line + ';level-' + str(level) + ';block-' + str (block_num)  + ';' #<<<<Testing - comment this line out!!
        if match:
            indent_level = match.start()
        #print (indent_level)
        #if (indent_level): print(f'{line} : is indented: {indent_level}')
        if (indent_level > level ):
            if (new_sub_block is False  and match.group() in BLOCKS): 
                new_sub_block = True #We now have a new sub-block starting
                sub_block_orig_lines = []
                block_num += 1 #Increment the block number
                sub_block_level = indent_level
            if (new_sub_block is True):    
                sub_block_orig_lines.append(line) #Add current line to the new sub-block
            else:
                main_block_orig_lines.append(line) #Add current line to the main block   
        else:
            if (new_sub_block is True):
                #We have just finished processing a sub-block and have returned to the main block
                sub_block_processed_lines = process_blocks(sub_block_orig_lines,sub_block_level)
                main_block_orig_lines = main_block_orig_lines + sub_block_processed_lines
                # for sub_block_processed_line in sub_block_processed_lines:
                #     main_block_orig_lines.append(sub_block_processed_line)
                new_sub_block = False #Reset sub-block as any sub-blocks we find after this will be new
            main_block_orig_lines.append(line)
    
    #We're done looping through the main block at this level        
    lines= [] #Free up some memory as we now have all the required lines in main_block_orig_lines

    #>>>>>>>>>>>>>Now call function to process the main block at this level<<<<<<<<<<<<<<<<<<
    replace_keyword_in_block(main_block_orig_lines, level) 

    return   main_block_orig_lines #main_block_processed_lines



def main():
    #code_lines =  code.split('\n')
    #exec (code)
    #print(process_blocks(code_lines, 0))
    code = open(sys.argv[1], 'r')
    code_lines = code.readlines()
    awesome = process_blocks(code_lines, 0)
    code.close()
    code = open(sys.argv[1], 'w')
    code.writelines(awesome)
main() 
