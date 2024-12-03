import os
import pandas as pd
from analysis.data_loader import DataLoader
from config import Config

def load_and_save_data(data_group):
    data_loader = DataLoader(Config.get_input_subdir(data_group), data_group=data_group)
    data_loader.save_extracted_data()
    return data_loader.get_data()

if __name__ == "__main__":
    positive_data = load_and_save_data('positive')
    negative_data = load_and_save_data('negative')
    
    all_data = positive_data + negative_data
    
    combined_df = pd.concat([participant_data.data for participant_data in all_data])
    combined_df = combined_df.round(3)
    # Save the combined DataFrame in the output/extracted_data folder
    output_dir = Config.get_output_subdir('extracted_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'qsvr_data.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Combined data saved to {output_path}")