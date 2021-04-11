from termcolor import colored
import json

def print_debug(string, color):
    print(colored(string,color))
    f = open("./file/DEBUG.txt","a",encoding="utf-8")
    f.write(string+"\n")
    f.close()

def found_data(file_path, data_name):
    try:
        f = open(file_path,"r",encoding="utf-8")
        data = json.loads(f.read())
        f.close()
        return data.get(data_name)
    except:
        print("[found_data] no data found", "red")
        return None

def write_data(file_path, data_name, value):
    try:
        f = open(file_path,"r",encoding="utf-8")
        data = json.loads(f.read())
        f.close()
        f = open(file_path,"w",encoding="utf-8")
        data[data_name] = value
        f.write(json.dumps(data))
        f.close()
    except:
        print_debug("[write_data] failed to write data", "red")