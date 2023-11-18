import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

from config import Config

def generate_plots(csv_file_path, output_dir, zip_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, header=None)

    # Create a directory to store the plots
    os.makedirs(output_dir, exist_ok=True)

    # Generate 36 plots with the final specifications
    for i, row in df.iloc[:36].iterrows():
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Plot the positions of each object
        ax.scatter(row[0], row[2], c='blue', s=50)
        ax.scatter(row[3], row[5], c='gray', s=50)
        ax.scatter(row[6], row[8], c='purple', s=50)
        ax.scatter(row[9], row[11], c='yellow', s=50)
        
        # Add text "VR" at position (0,0)
        ax.text(0, 0, 'VR', fontsize=12, ha='center', va='center')
        
        # Draw the circle with specified diameter and center
        main_circle = plt.Circle((3, -4), 7/2, color='black', fill=False, linewidth=2)
        ax.add_artist(main_circle)
        
        # Draw the modified rectangle
        rectangle = plt.Polygon([[-1.5, 0.5], [-1.5, -9], [12, -9], [12, 0.5]], closed=True, edgecolor='black', linewidth=2, fill=False)
        ax.add_artist(rectangle)
        
        # Add two new circles with line color cyan
        circle1 = plt.Circle((2, 1), 0.5/2, color='cyan', fill=False, linewidth=2)
        ax.add_artist(circle1)
        
        circle2 = plt.Circle((-2, -2), 0.5/2, color='cyan', fill=False, linewidth=2)
        ax.add_artist(circle2)
        
        # Set title, axis labels, and axis limits
        ax.set_title(f"Line Number: {i+1}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Z Coordinate")
        
        # Explicitly setting the axis limits
        ax.set_xlim(-3, 13)
        ax.set_ylim(-10, 3)
        
        # Set equal aspect ratio after setting axis limits
        ax.set_aspect('equal', adjustable='box')
        
        # Save the plot to the directory
        plt.savefig(f"{output_dir}/plot_{i+1}.png")
        plt.close()

    # Zip all the plots
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), file)

if __name__ == "__main__":
    csv_file_path = Config.OBJECT_CONFIGURATION_CSV_FILE_PATH
    output_dir = Config.get_output_subdir("objectconfigurations")
    zip_file_path = os.path.join(output_dir,'configurations.zip')
    
    generate_plots(csv_file_path, output_dir, zip_file_path)