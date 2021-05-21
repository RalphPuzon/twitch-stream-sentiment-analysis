import json, ast
import pandas as pd

#this is to handle the json string 
null = ""
true = True
false = False
with open("05-15-2021_x_backsmasherrr.json", 'r', encoding='utf-8') as f:
    for line in f:
        x = eval(ast.literal_eval(json.dumps(line)))
        print(x)
        

        

        

        