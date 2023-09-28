import matplotlib.pyplot as plt
import numpy as np
import math
import os

grid_images_dir = os.path.join('static', 'images', 'grid_images')
os.makedirs(grid_images_dir, exist_ok=True)

def create_match_grids(data, match_id):
    nw_data = data["radiantNetworthLead"]
    exp_data = data["radiantExperienceLead"]

    """
    First we need to find if the positive or negative number is furthest away from zero.
    Then we round the number up/down to closest 5000 to make the diagram look good.
    The creating the plot we generate the y ticks to ensure an even y axis.
    """

    # find number that is furthest away from 0
    def furthest_from_zero(a, b):
        distance_a = abs(a - 0)
        distance_b = abs(b - 0)

        if distance_a > distance_b:
            return a
        elif distance_b > distance_a:
            return b
        else:
            return a

    # round up/down to closest 5000
    def round_up_to_5000(number):
        if number >= 0:
            return int(math.ceil(number / 5000.0)) * 5000
        else:
            new_num = int(math.ceil((number*-1) / 5000.0)) * 5000
            return new_num

    # find number furthest from zero and round up
    def furthestFromZero(data):
        num1, num2 = min(data), max(data)
        result = furthest_from_zero(num1, num2)
        rounded_result = round_up_to_5000(result)
        return rounded_result


    # function for Networth grid
    def create_NW_plot(nw_data):
        curr_result = furthestFromZero(nw_data)
        minutes = list(range(len(nw_data)))
        plt.figure(figsize=(10, 6))

        # set different color on all the values to display what team is leading
        for i in range(len(nw_data)-1):
            if nw_data[i] >= 0:
                plt.plot([minutes[i], minutes[i+1]], [nw_data[i], nw_data[i+1]], marker='o', linestyle='-', color='green')
            else:
                plt.plot([minutes[i], minutes[i+1]], [nw_data[i], nw_data[i+1]], marker='o', linestyle='-', color='red')

        plt.title('Networth Lead Over Time')
        plt.xlabel('Time (Minutes)')
        plt.ylabel('Networth Lead')

        # Set custom y-axis tick positions
        y_ticks = np.arange(-curr_result, curr_result+5000, 5000)
        plt.yticks(y_ticks)

        plt.grid(True)
        # save as image file (png)
        plt.savefig(f'static/images/grid_images/{match_id}_NW.png', dpi=300, format='png')


    # function for Experience grid
    def create_EXP_plot(exp_data):
        curr_result = furthestFromZero(exp_data)
        minutes = list(range(len(exp_data)))
        plt.figure(figsize=(10, 6))

        # set different color on all the values to display what team is leading
        for i in range(len(nw_data)-1):
            if nw_data[i] >= 0:
                plt.plot([minutes[i], minutes[i+1]], [exp_data[i], exp_data[i+1]], marker='o', linestyle='-', color='green')
            else:
                plt.plot([minutes[i], minutes[i+1]], [exp_data[i], exp_data[i+1]], marker='o', linestyle='-', color='red')

        plt.title('Experience Lead Over Time')
        plt.xlabel('Time (Minutes)')
        plt.ylabel('Experience Lead')

        # Set custom y-axis tick positions
        y_ticks = np.arange(-curr_result, curr_result+5000, 5000)
        plt.yticks(y_ticks)

        plt.grid(True)
        # save as image file (png)
        plt.savefig(f'static/images/grid_images/{match_id}_EXP.png', dpi=300, format='png')
        

    create_NW_plot(nw_data)
    create_EXP_plot(exp_data)