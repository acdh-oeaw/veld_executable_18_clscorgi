import csv
import os
import sys


# some tsv were too big, so increase max memory allocation of csv module
csv.field_size_limit(sys.maxsize)


def get_conllu_data(repo_id: str, stem: str) -> dict:
    """main function for conllu processing, takes repo_id and stem and returns conllu statistics"""
    
    # returned dictionary, defined here for communication of its structure
    result_dict = {
        "token_count": None,
    }
    
    def read_file():
        """find conllu file given repo_id and stem, and return its content as a list of rows"""
        
        # find folder
        conllu_folder_path = None
        for eltec_folder in os.listdir("/veld/input/data/"):
            if eltec_folder.lower() == repo_id:
                conllu_folder_path = f"/veld/input/data/{eltec_folder}/level1"
                
        # find file
        conllu_file_path =None
        for eltec_file in os.listdir(conllu_folder_path):
            if eltec_file.lower().split(".conllu")[0] == stem:
                conllu_file_path = conllu_folder_path + "/" + eltec_file
                
        # read file
        with open(conllu_file_path, "r") as f:
            return list(csv.reader(f, delimiter="\t"))
                        
    def process_conllu_content(conllu_content, result_dict):
        """process conllu content"""
        
        # statistics of interest
        token_count = 0
        
        # main loop over rows, create statistics
        for row in conllu_content:
            if len(row) != 0 and not row[0].startswith("#"):
                token_count += 1
                
        # load statistics into dict, return
        result_dict["token_count"] = token_count
        return result_dict
    
    # main calls and return
    conllu_content = read_file()
    result_dict = process_conllu_content(conllu_content, result_dict)
    return result_dict
