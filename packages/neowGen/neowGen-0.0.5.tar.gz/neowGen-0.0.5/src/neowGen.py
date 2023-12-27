import os
import pandas as pd
from tqdm import tqdm
import huggingface_hub
from datasets import Dataset
import csv
class datasetGenerator:

    
    # Define the model type and affects the corresponding tokens
    def __setModel(self) -> None:

        if(self.model_type==""):
            return
        f= self.dict_formats.get(self.model_type,None)
        if(f==None):
            return
        f()
        
       
    def alpaca(self):
        self.sos = ""
        self.eos = ""
        self.sys = ""
        self.esys = ""
        self.inst = "[INST]"
        self.einst="[/INST]"
        self.assistant = ""
        self.eassistant = ""
        return
    
   

    

    #used for generic context passed to the prompt
    def setlocalContext(self,local_context) -> None:
        self.local_context = local_context
        
    def setglobalContext(self,global_context) -> None:
        self.global_context = global_context   
    
    #Let's build the prompt by passing the tokens defined by the model
    def generate_prompt(self,global_context="",local_context="",question="",answer="",verbose=False) ->str:
        full_prompt =self.sos
        full_prompt += self.sys
        full_prompt += global_context
        full_prompt += self.esys
        full_prompt += self.inst
        full_prompt += local_context + " "
        if(verbose):
            print(question)
        full_prompt += question
        full_prompt += self.einst
        full_prompt += self.assistant
        full_prompt += answer
        full_prompt += self.eassistant
        full_prompt += self.eos
        return full_prompt
    
    #initialize the generator
    def __init__(self,model_type:str ="") -> None:
        self.dataframes = {}
        self.sos = ""
        self.eos = ""
        self.sys = ""
        self.esys = ""
        self.inst = ""
        self.einst=""
        self.assistant = ""
        self.eassistant = ""
        self.global_context = ""
        self.local_context = ""
        
        self.dict_formats = {
            "code llama instruct": self.alpaca,
            "alpaca": self.alpaca,
            "mistral instruct": self.alpaca,
        }
        self.model_type = model_type
        self.__setModel()

    
    def check_csv(self,csv_file:str) -> bool:
        try:
            with open(csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                expected_columns = ["question", "answer"]

                for row in reader:
                # Make sure question and answer columns exist
                    if not all(column in row for column in expected_columns):
                        print(f"{csv_file} Error : The file should contain the following columns: {', '.join(expected_columns)}")
                        return False

                    if not all(row[column] for column in expected_columns):
                        print(f"{csv_file} Error : incorrect line :\n{row}")
                        return False

            return True
        except csv.Error as e:
            print(f"{csv_file} Error reading CSV : {e}")
            with open(csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                line_number = 0
                for row in reader:
                    line_number += 1
                    try:
                        # check nb of rows
                        if len(row) != 2:
                            raise csv.Error(f"{csv_file} Incorrect number of columns line {line_number}: {row}")
                            return False

                    except csv.Error as e:
                        print(f"{csv_file} Line {line_number} is generating an error : {e}\nwith row : {row}") 
                        return False
            return False
        
    #Generate a dict of DF from a directory
    def generate_from_corpus(self,base_dir:str = 'corpus',verbose=True) -> bool:
        self.dataframes = {}
        df_count = 0
        csv_counts = {}

        for root, dirs, files in os.walk(base_dir):
            csv_files = [f for f in files if f.endswith('.csv')]
            df_list = []

            for csv_file in csv_files:
                file_path = os.path.join(root, csv_file)

                if not self.check_csv(file_path):
                    return False

                try:
                    df = pd.read_csv(file_path)
                    df_list.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    return False

            if df_list:
                combined_df = pd.concat(df_list, ignore_index=True)
                subdir = os.path.relpath(root, base_dir)  # Get relative path as subdir name
                self.dataframes[subdir] = combined_df
                df_count += 1
                csv_counts[subdir] = len(df_list)

        if verbose:
            print(f"Number of dataframes created: {df_count}")
            for subdir, count in csv_counts.items():
                print(f"Number of CSV files read for '{subdir}' dataframe: {count}")

        return True            
    
    def generate_dataset(self,verbose=False) -> None:
        for key, dataframe in self.dataframes.items():
            print(f"Generating prompt for dataset '{key}':")
            
            #Check if the 'question' and 'answer' columns exist
            if 'question' not in dataframe.columns:
                print(f"'question' column is not in '{key}' dataset!")
                return
            if 'answer' not in dataframe.columns:
                print(f"'answer' column is not in '{key}' dataset!")
                return
            
            #Then generate the text column 
            dataframe['text'] = dataframe.apply(lambda row: self.generate_prompt(
                self.global_context,self.local_context,
                question=row['question'], answer=row['answer'],verbose =verbose), axis=1)
            
            #and drop the source columns
            dataframe.drop(["question","answer"], axis=1, inplace=True)
    
    # Save the dataset to disk in a compressed format
    def save_to_disk(self,directory ="") -> None:
        
        if not directory.endswith('/'):
            directory+= "/"
            
        for key, dataframe in self.dataframes.items():
            dataset = Dataset.from_pandas(dataframe)
            dataset.save_to_disk(directory + "ds_" + key)
            
    # Push the dataset to the Hugging face hub
    def push_to_hub(self,name ="")  -> None:
        for key, dataframe in self.dataframes.items():
            
            try:
                dataset= Dataset.from_pandas(dataframe)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return
                
            try:
                dataset.push_to_hub(name,split=key)
            except ConnectionError:
                print("Error: Failed to connect. Please check your internet connection.")
                return
            except PermissionError:
                print("Error: You don't have the necessary permissions to push to this repository.")
                return
            except ValueError:
                print("Error: Invalid arguments provided.")
                return
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return
                
            print(f"->Dataset '{key}' pushed to hub {name}")