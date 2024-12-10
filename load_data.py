import os
import pandas as pd
from analysis.data_loader import DataLoader
from config import Config
from analysis.objects_configurator import ObjectConfigurator

def order_positions(positions):
    """
    Order a set of positions based on the x-coordinate.
    
    Args:
    - positions (list): A list of dictionaries containing 'real_x' and 'real_z' keys,
                        or a list of tuples containing (x, z) coordinates.

    Returns:
    - list: A list of positions ordered by the x-coordinate.
    """
    if isinstance(positions[0], dict):
        return sorted(positions, key=lambda x: x['real_x'])
    elif isinstance(positions[0], tuple):
        return sorted(positions, key=lambda x: x[0])
    else:
        raise ValueError("Unsupported position format")

def match_object_positions(df, object_positions_from_configurator):
    # Match object configurations from configurator to participant data
    matches = []
    for _, participant_data in df.groupby(['participant_id']):
        for trial_num_tuple, trial_data in participant_data.groupby(['trial_num']):
            trial_num = trial_num_tuple[0]  # Extract the trial number from the tuple
            participant_config = trial_data[['real_x', 'real_z']].to_dict('records')
            ordered_participant_config = order_positions(participant_config)
            for line_num, configurator_config in enumerate(object_positions_from_configurator, 1):
                ordered_configurator_config = order_positions(list(configurator_config))
                if ordered_participant_config == [{'real_x': x, 'real_z': z} for x, z in ordered_configurator_config]:
                    matches.append((participant_data['participant_id'].iloc[0], trial_num, line_num))
                    break
    
    # Create a DataFrame with the matched data
    match_df = pd.DataFrame(matches, columns=['participant_id', 'trial_num', 'configurator_line'])
    
    # Merge the matched data with the original DataFrame
    merged_df = pd.merge(df, match_df, on=['participant_id', 'trial_num'])
    
    return merged_df

def load_and_save_data(data_group):
    data_loader = DataLoader(Config.get_input_subdir(data_group), data_group=data_group)
    data_loader.save_extracted_data()
    return data_loader.get_data()

def process_data_groups():
    positive_data = load_and_save_data('positive')
    negative_data = load_and_save_data('negative')
    
    all_data = positive_data + negative_data
    
    combined_df = pd.concat([participant_data.data for participant_data in all_data])
    combined_df = combined_df.round(3)
    
    # Read object positions from the configurator
    object_configurator = ObjectConfigurator()
    object_configurator.read_positions()
    object_positions_from_configurator = object_configurator.csv_positions

    # Match object positions and add the 'configurator_line' column
    combined_df = match_object_positions(combined_df, object_positions_from_configurator)

    # Create the 'object_configuration_type' column based on 'configurator_line'
    combined_df['object_configuration_type'] = combined_df['configurator_line'].apply(lambda x: 'open' if x > 12 else 'closed') 

    # Save the combined DataFrame in the output/extracted_data folder
    output_dir = Config.get_output_subdir('extracted_data')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'qsvr_data.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Combined data saved to {output_path}")

if __name__ == "__main__":
    process_data_groups()
