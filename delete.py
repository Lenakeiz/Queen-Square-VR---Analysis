import numpy as np
import matplotlib.pyplot as plt

def calculate_average_angle(angles_degrees):
    # Convert degrees to radians
    angles_radians = np.deg2rad(angles_degrees)
    
    # Convert to unit circle representation
    unit_vectors = np.exp(1j * angles_radians)
    
    # Calculate the mean of these unit vectors
    mean_vector = np.mean(unit_vectors)
    
    # Get the angle of the resultant vector
    mean_angle_radians = np.angle(mean_vector)
    mean_angle_degrees = np.rad2deg(mean_angle_radians)
    
    return mean_angle_degrees

# Example usage
angles_degrees_1 = np.array([0, 90, 180, -90])
mean_angle_1 = calculate_average_angle(angles_degrees_1)
print("Average Angle for Example 1 in Degrees:", mean_angle_1)

angles_degrees_2 = np.array([0, 90, 180, 270])
mean_angle_2 = calculate_average_angle(angles_degrees_2)
print("Average Angle for Example 2 in Degrees:", mean_angle_2)

# Plotting function
def plot_angles(angles_degrees, mean_angle, title):
    angles_radians = np.deg2rad(angles_degrees)
    mean_angle_radians = np.deg2rad(mean_angle)
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    for angle in angles_radians:
        ax.plot([0, angle], [0, 1], marker='o')
    ax.plot([0, mean_angle_radians], [0, 1], marker='o', color='red', linewidth=2, label='Mean Angle')
    ax.set_title(title)
    ax.legend()
    plt.show()

plot_angles(angles_degrees_1, mean_angle_1, 'Example 1: [0, 90, 180, -90]')
plot_angles(angles_degrees_2, mean_angle_2, 'Example 2: [0, 90, 180, 270]')