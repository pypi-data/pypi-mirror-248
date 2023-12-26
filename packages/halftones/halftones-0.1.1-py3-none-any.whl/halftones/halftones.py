"""
halftones.py
------------

Description:
    A module for generating and manipulating halftone images. This module includes
    functions for creating synthetic RGB images, plotting CMYK channels, calculating
    image DPI, and generating halftone patterns.

Author: Erkin Otles
Created: December 18, 2023
Last Modified: December 18, 2023

"""

import argparse
import cv2
import math
import matplotlib.collections
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# Generating a synthetic RGB image for demonstration
def generate_synthetic_image():
    """
    Generates a synthetic RGB image for demonstration.
    
    Returns:
        Image: A PIL Image object with predefined RGB colors.
    """
    # Create an RGB image with different colors
    red, green, blue = (255, 0, 0), (0, 255, 0), (0, 0, 255)
    image_data = np.zeros((100, 100, 3), dtype=np.uint8)

    # Red square
    image_data[25:75, :50] = red
    # Green square
    image_data[25:75, 50:] = green
    # Blue corner
    image_data[:25, :25] = blue

    return Image.fromarray(image_data)


def plot_cmyk_channels(cmyk_image):
    """
    Plots the CMYK channels of a given CMYK image.
    
    Args:
        cmyk_image (Image): A PIL Image object in CMYK mode.
    """
    # Split the CMYK image into its four channels
    c, m, y, k = cmyk_image.split()

    # Create a list of channels and their corresponding titles
    channels = [c, m, y, k]
    titles = ['Cyan Channel', 'Magenta Channel', 'Yellow Channel', 'Black Channel']

    # Plot each channel
    plt.figure(figsize=(12, 6))
    for i, (channel, title) in enumerate(zip(channels, titles)):
        plt.subplot(1, 4, i+1)
        plt.imshow(channel, cmap='gray')
        plt.title(title)
        plt.axis('off')
    plt.tight_layout()
    plt.show()


def get_image_dpi(image, dpi_default=256):
    """
    Retrieves the DPI of an image, or sets a default value if not available.
    
    Args:
        image (Image): A PIL Image object.
        dpi_default (int, optional): Default DPI value. Defaults to 256.
    
    Returns:
        float: The DPI of the image.
    """
    try:
        # Attempt to extract DPI from the image's info dictionary
        dpi = image.info.get('dpi', (dpi_default, dpi_default))  # Default to dpi_default if not found
        return float(dpi[0])  # Convert to float and return the first value (horizontal DPI)
    except AttributeError:
        # If the image doesn't have the 'info' attribute or DPI info
        return dpi_default  # Default DPI value


def find_lines(theta_deg, rectangle_width, rectangle_height, grid_width):
    """
    Finds lines with a given angle that intersect and envelop a rectangle.

    Args:
        theta_deg (float): The angle of the line in degrees.
        rectangle_width (int): The width of the rectangle.
        rectangle_height (int): The height of the rectangle.
        grid_width (float): The distance between parallel lines.

    Returns:
        tuple: A tuple containing the slope, original y-intercept, and a list of y-intercepts for parallel lines.
    """
    # Convert theta from degrees to radians
    theta_rad = np.radians(theta_deg)

    # Calculate the slope
    m = np.tan(theta_rad)

    # Center of the rectangle
    x_center, y_center = rectangle_width / 2, rectangle_height / 2

    # Calculate the y-intercept of the original line
    c_original = y_center - m * x_center

    
    # Function to calculate y-intercept for parallel lines
    def calculate_new_c(c, distance):
        return c - distance * np.sqrt(1 + m**2)

    # Function to check if new line intersects with rectangle
    def check_c_intersects(c_new):
        y_left = c_new
        y_right = m*rectangle_width + c_new
        
        y_max = max(y_left, y_right)
        y_min = min(y_left, y_right)
        return (0 <= y_left <= rectangle_height ) or (0 <= y_right <= rectangle_height ) or \
            (y_min<rectangle_height and y_max>rectangle_height)
        
    all_c = [c_original]
    i = -1
    while True:
        c_new = calculate_new_c(c_original, i * grid_width)
        all_c.append(c_new)
        i=i-1
        if check_c_intersects(c_new)==False:
            break
    i = 1
    while True:
        c_new = calculate_new_c(c_original, i * grid_width)
        all_c.append(c_new)
        i=i+1
        if check_c_intersects(c_new)==False:
            break
    return (m, c_original, sorted(all_c))


def grid_lines(theta_deg, image, grid_width, display_flag=False):
    """
    Draws grid lines on an image based on a specified angle.

    Args:
        theta_deg (float): The angle of the grid lines in degrees.
        image (Image): A PIL Image object.
        grid_width (float): The width of the grid.
        display_flag (bool, optional): Flag to display the image with grid lines. Defaults to False.

    Returns:
        tuple: A tuple containing information about the normal and orthogonal lines.
    """
    normal_line_info = find_lines(theta_deg, image.width, image.height, grid_width)
    orthog_line_info = find_lines(90+theta_deg, image.width, image.height, grid_width)

    if display_flag:
        # Create a figure and axis for plotting
        fig, ax = plt.subplots()
        ax.imshow(image, cmap='gray_r')
        ax.set_xlim([-20, image.width+20])
        ax.set_ylim([-20, image.height+20])
        ax.set_aspect('equal', adjustable='box')

        rectangle = plt.Rectangle((0, 0), image.width, image.height, fill=False)
        ax.add_patch(rectangle)
        
        # Plot the original line and its parallels
        x_values = np.linspace(-100, image.width+100, 500)
        m, c_original, all_c = normal_line_info
        for c in all_c:
            y_values = m * x_values + c
            ax.plot(x_values, y_values, 'b--' if c != c_original  else 'b-')  # Red for the original line, blue for parallels
            
        m, c_original, all_c = orthog_line_info
        for c in all_c:
            y_values = m * x_values + c
            ax.plot(x_values, y_values, 'r--' if c != c_original  else 'r-')  # Red for the original line, blue for parallels
            
        
        # Set title and labels
        ax.set_title(f'Normal ({theta_deg}°) & orthogonal lines through image')
        ax.invert_yaxis()
        
        # Show the plot
        plt.show()
    
    return (normal_line_info, orthog_line_info)


def get_tile_info(theta_deg, greyscale_image, grid_width, display_flag=False):
    """
    Calculates information about tiles formed by intersecting lines on an image.

    Args:
        theta_deg (float): The angle of the intersecting lines in degrees.
        greyscale_image (Image): A greyscale PIL Image object.
        grid_width (float): The width of the grid.
        display_flag (bool, optional): Flag to display the image with tiles. Defaults to False.

    Returns:
        dict: Dictionary containing information about each tile.
    """

    # Get line information for normal and orthogonal lines based on the specified angle
    normal_line_info, orthog_line_info = grid_lines(theta_deg, 
                                                    greyscale_image, 
                                                    grid_width,
                                                    display_flag=display_flag
                                                   )
    normal_m, _, normal_all_c = normal_line_info
    orthog_m, _, orthog_all_c = orthog_line_info

    # Function to find the intersection point of two lines
    def find_intersection(m1, c1, m2, c2):
        """Find the intersection point of two lines."""
        if m1 == m2:  # Parallel lines
            return None
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        return [x, y]

    # Convert the greyscale image to a NumPy array for processing
    greyscale_image_np = np.array(greyscale_image)

    # Get the dimensions of the image
    image_width, image_height = greyscale_image.size

    # Initialize a dictionary to store tile information
    tiles = {}

    # Pairs of normal and orthogonal lines to generate tiles
    # Loop through each set of normal lines
    prev_normal_c = normal_all_c[0]
    for curr_normal_c in normal_all_c[1:]:

        # Loop through each set of orthogonal lines
        prev_orthog_c = orthog_line_info[0]
        for curr_orthog_c in orthog_all_c[1:]:

            # Calculate the intersection points of the four lines
            intersections = np.array([
                find_intersection(normal_m, prev_normal_c, orthog_m, prev_orthog_c),
                find_intersection(normal_m, prev_normal_c, orthog_m, curr_orthog_c),
                find_intersection(normal_m, curr_normal_c, orthog_m, prev_orthog_c),
                find_intersection(normal_m, curr_normal_c, orthog_m, curr_orthog_c)]
            )
            
            # Calculate the center of the tile
            center = intersections.mean(0)

            # Check if the tile center is within the boundaries (1 grid_width away from image borders)
            if (-grid_width <= center[0] < image_width+grid_width) and (-grid_width <= center[1] < image_height+grid_width):

                # Need to reorder points in order to ensure that they are not kitty-corner
                # Calculate the angle from centroid to each vertex
                angles = np.arctan2(intersections[:, 1] - center[1], 
                                    intersections[:, 0] - center[0])
            
                # Sort vertices based on the calculated angles
                sorted_indices = np.argsort(angles)
                sorted_intersections = intersections[sorted_indices]
        
                # Define vertices for the tile
                trapezoid_vertices = np.array(sorted_intersections, dtype=np.int32)
        
                # Create a mask for the tile
                mask = np.zeros(greyscale_image_np.shape, dtype=np.uint8)
                cv2.fillPoly(mask, [trapezoid_vertices], 1)
                
                # Apply the mask to the image to isolate the tile area
                trapezoid_area = cv2.bitwise_and(greyscale_image_np, 
                                                 greyscale_image_np, 
                                                 mask=mask)
                
                # Calculate the average pixel value within the tile
                average_value = np.mean(trapezoid_area[mask == 1])

                # Store the calculated tile information
                tiles[tuple(center)] = {
                    'intersections': sorted_intersections,
                    'vertices': trapezoid_vertices,
                    'value': average_value
                }

            # Update the previous lines for the next iteration
            # Update previous orthogonal line to be the current one
            prev_orthog_c = curr_orthog_c
        # Update previous normal line to be the current one    
        prev_normal_c = curr_normal_c

    return tiles


def extract_black_channel(grayscale_image, black_channel_threshold=128):
    """
    Extracts a black channel from a grayscale image based on a threshold.

    Args:
        grayscale_image (Image): A grayscale PIL Image object.
        threshold (int): Pixel value threshold for determining black.

    Returns:
        Image: A PIL Image object representing the black channel.
    """
    # Convert the image to a NumPy array for processing
    grayscale_np = np.array(grayscale_image)

    # Initialize an array for the black channel
    black_channel = np.zeros_like(grayscale_np)

    # Assign values to the black channel based on the threshold
    black_channel[grayscale_np < black_channel_threshold] = 255 - grayscale_np[grayscale_np < black_channel_threshold]

    # Convert back to a PIL Image and return
    return Image.fromarray(black_channel)



def setup_fig_ax(image, dpi_default=256, display_flag=True,
                 display_white_background_flag=True):
    """
    Sets up a matplotlib figure and axis for plotting.

    Args:
        image (Image): A PIL Image object.
        dpi_default (int, optional): Default DPI value. Defaults to 256.
        display_flag (bool, optional): Flag to display additional information. Defaults to True.
        display_white_background_flag (bool, optional): Flag to set white background. Defaults to True.

    Returns:
        tuple: A tuple containing the matplotlib figure and axis.
    """
    if display_flag: print('Image size: {}'.format(image.size))

    # Get DPI
    dpi = get_image_dpi(image, dpi_default=dpi_default)
    if display_flag: print('DPI: {}'.format(dpi))

    # Calculate figure size in inches (width and height in pixels / dpi)
    fig_width, fig_height = 4*float(image.width) / dpi, 4*float(image.height) / dpi
    if display_flag: print('Figure size: {}'.format((fig_width, fig_height)))
        
    # Create a figure and axis for further plotting
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
    ax.axis('off')
        
    # Set white background if requested
    if display_white_background_flag:
        white_image = np.zeros([image.height, image.width, 3], dtype=np.uint8)
        white_image.fill(255)
        ax_image = ax.imshow(white_image, zorder=-1)  # Set zorder to -1
    else:
        ax_image = ax.imshow(image, zorder=-1)  # Set zorder to -1

    # Do not display the figure
    plt.close(fig)
                     
    return fig, ax


def save_fig_and_display_image(fig, image_name, display_flag):
    """
    Saves a matplotlib figure as an image and optionally displays it.

    Args:
        fig (matplotlib.figure.Figure): The matplotlib figure to save.
        image_name (str): The name of the file to save the image as.
        display_flag (bool): Flag to display the image.
    """
    # Save the plot as an image file with tight bounding box and no padding
    fig.savefig(image_name, bbox_inches='tight', pad_inches=0)
    fig.clf()  # Clear the figure to free up memory

    def display_with_browser(image_name):
        import os
        import webbrowser
        # Open the image file with the default image viewer
        webbrowser.open('file://' + os.path.realpath(image_name))

    # Display the image if requested
    if display_flag:
        try:
            from IPython.display import Image as IPImage
            display(IPImage(filename=image_name))
        except ImportError:
            # IPython is not available, open image using a standard library
            display_with_browser(image_name)
        except NameError:
            # Not in an IPython environment; use a standard method to open the image
            display_with_browser(image_name)




def generate_halftone_image(image, grid_width=None, display_flag=True,
                            black_channel_threshold=None, #lower means that it has to be more black to be included
                            halftone_alpha=2/3,
                            halftone_image_name='halftone_image.png',
                            dpi_default=256,
                            display_white_background_flag=True
                           ):
    """
    Generates a halftone image from the given image.
    
    Args:
        image (Image): A PIL Image object.
        grid_width (float, optional): The distance between lines.
            Calculated based on image width if None.
        display_flag (bool, optional): Whether to display the image. Defaults to True.
        black_channel_threshold (int, optional): Threshold for black channel extraction.
            Lower value means only darker areas are included. None means default CMYK conversion.
        halftone_alpha (float, optional): Alpha value for halftone effect. Defaults to 2/3.
        halftone_image_name (str, optional): Filename for the halftone image. Defaults to 'halftone_image.png'.
        dpi_default (int, optional): Default DPI value. Defaults to 256.
        display_white_background_flag (bool, optional): Whether to display a white background. Defaults to True.
    
    Returns:
        dict: Information about the color channels and their tiles.
    """
    fig, ax = setup_fig_ax(image, dpi_default=dpi_default, 
                           display_flag=display_flag,
                        display_white_background_flag=display_white_background_flag)
                        
    if grid_width is None:
        grid_width = image.width/20
        if display_flag: print('Set grid_width to: {:.2f}'.format(grid_width))

    if display_flag: print('Image array shape: {}'.format(np.array(image).shape))

    # Seperate into channels
    if display_flag: print("Creating channels...")
    image_cmyk = image.convert('CMYK')
    c, m, y, k = image_cmyk.split()

    # Replace the K channel with a custom-extracted black channel if a threshold is provided
    if black_channel_threshold is not None:
        # Replace the K channel with a custom-extracted black channel
        k = extract_black_channel(image.convert("L"),
                                  black_channel_threshold=black_channel_threshold)
    
    color_info = {
        'yellow': {'image': y, 'angle': 0.001}, 
        #yellow is technically 0, but perfectly vertical lines are weird for math
        #they ended up making too many dots on the center vertical
        'cyan': {'image': c, 'angle': 15},
        'magenta': {'image': m, 'angle': 45},
        'black': {'image': k, 'angle': 75}
    }

    # Compute tile info
    if display_flag: print("Computing tile info...")
    for color, color_dict in color_info.items():
        if display_flag: print("\t{}...".format(color))
        color_tile_info = get_tile_info(color_dict['angle'], 
                                        color_dict['image'], 
                                        grid_width,
                                        display_flag=display_flag)
        color_dict['tile_info'] = color_tile_info
        if display_flag: print("\tn tiles: {}".format(len(color_tile_info)))

    if display_flag: print("Generating image...")
    for color, color_dict in color_info.items():
        color_circles = []
        for tile_center, tile_info in color_dict['tile_info'].items():
            if math.isnan(tile_info['value'])==False:
                tile_width = (tile_info['value']/255)*(grid_width)
                tile_circle_radius = (tile_info['value']/255)*(grid_width)

                # Create a circle and add it to the list
                tile_circle = plt.Circle(tile_center, radius=(tile_width/2))
                color_circles.append(tile_circle)
                
        # Create a PatchCollection from the list of circles                
        color_circle_collection = matplotlib.collections.PatchCollection(
            color_circles, 
            facecolors=color,
            alpha=halftone_alpha)
        # Add the collection to the axes instead of the global plot
        ax.add_collection(color_circle_collection)

    save_fig_and_display_image(fig, halftone_image_name, display_flag)
    return color_info



def check_color_tiles(color_info, image, colors=['yellow'], tile_shape='rect',
                      grid_width=None,
                      tile_alpha=2/3,
                      display_flag=True,
                      display_white_background_flag=True,
                      dpi_default=256,
                      color_tiles_image_name='color_tiles_image.png'):
    """
    Checks and visualizes color tiles based on provided color information.
    It allows for different shapes and configurations of tiles.

    Args:
        color_info (dict): Dictionary containing color information and tile data.
        image (Image): A PIL Image object.
        colors (list, optional): List of colors to be checked. Defaults to ['yellow'].
        tile_shape (str, optional): Shape of the tiles, 'rect' or 'circle'. Defaults to 'rect'.
        grid_width (float, optional): Distance between lines in the halftone pattern.
            Defaults to None, which sets it based on image width.
        tile_alpha (float, optional): Alpha (transparency) value for the tiles. Defaults to 2/3.
        display_flag (bool, optional): Flag to display the image. Defaults to True.
        display_white_background_flag (bool, optional): Flag to use a white background. Defaults to True.
        dpi_default (int, optional): Default DPI value for the image. Defaults to 256.
        color_tiles_image_name (str, optional): Filename to save the image. Defaults to 'color_tiles_image.png'.
    """
    # Set default line distance based on image width if not provided
    if grid_width is None:
        grid_width = image.width/20
        print('Set grid_width to: {:.2f}'.format(grid_width))

    # Set up figure and axis for plotting using the utility function
    fig, ax = setup_fig_ax(image, dpi_default=dpi_default, 
                           display_flag=display_flag,
                        display_white_background_flag=display_white_background_flag)

    # Iterate through each color to process its tiles
    for color in colors:
        angle = color_info[color]['angle']
        tile_patches = []

        # Iterate through each tile in the color's tile information
        for tile_center, tile_info in color_info[color]['tile_info'].items():
            # Check if the tile value is valid (not NaN)
            if math.isnan(tile_info['value'])==False:
                tile_width = (tile_info['value']/255)*(grid_width)
                tile_anchor = (tile_center[0]-tile_width/2, tile_center[1]-tile_width/2)

                # Create tile patch based on the specified shape
                if tile_shape == 'rect':
                    # Rectangle shape
                    tile_patch = plt.Rectangle(tile_anchor, tile_width, tile_width,
                                               angle=angle, rotation_point='center')
                elif tile_shape == 'circle':
                    # Circle shape
                    tile_patch = plt.Circle(tile_center, tile_width/2)
                
                # Add the tile patch to the list    
                tile_patches.append(tile_patch)

        # Create a collection of patches for the current color
        tile_collection = matplotlib.collections.PatchCollection(
            tile_patches, 
            facecolors=color,
            alpha=tile_alpha)
        # Add the collection to the plot
        ax.add_collection(tile_collection)

    # Save the figure as an image and display it if requested
    save_fig_and_display_image(fig, color_tiles_image_name, display_flag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a halftone image from an input image.")
    parser.add_argument("image_path", type=str, help="Path to the input image.")
    parser.add_argument("--grid_width", type=float, default=None, help="Distance between halftone lines.")
    parser.add_argument("--display", action="store_true", default=False, help="Display the generated image.")
    parser.add_argument("--halftone_alpha", type=float, default=2/3, help="Alpha value for halftone effect.")
    parser.add_argument("--output", type=str, default="halftone_image.png", help="Output filename for the halftone image.")
    parser.add_argument("--dpi", type=int, default=256, help="DPI value for the image.")
    parser.add_argument("--white_background", action="store_true", default=True, help="Use a white background for the image.")
    parser.add_argument("--black_channel_threshold", type=int, default=None, help="Threshold for black channel extraction.")


    args = parser.parse_args()

    input_image = Image.open(args.image_path)
    generate_halftone_image(
        input_image, 
        grid_width=args.grid_width, 
        display_flag=args.display,
        black_channel_threshold=args.black_channel_threshold,
        halftone_alpha=args.halftone_alpha,
        halftone_image_name=args.output,
        dpi_default=args.dpi,
        display_white_background_flag=args.white_background
    )
