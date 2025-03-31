""" The command line interface (CLI) parser """
from argparse import ArgumentParser, Namespace
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from lab8_compass import Compass
import numpy as np
from PySide6.QtCore import QTimer


class Accelaration_3D(FigureCanvas):
    def __init__(self, figure=None):
        super().__init__(figure)

        self.counter = 0.0
        self.value = 0.2 #0.1 step is very slow
        self.accela = round(float(input("Enter your accelaration value: ")),1)
        last_digit = self.accela*10
        last_digit = last_digit %10
        if last_digit % 2 != 0:
            self.accela += 0.1  #since the step is 0.2 we will make odd inputs into even.
            
        self.figure = Figure()
        self.ax = self.figure.add_subplot(projection='3d')

        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([-15, 15])
        self.ax.set_title("3D Acceleration")

        self.ax.view_init(azim=-115,elev=20,roll=3)


    def update_plot(self):
        
        self.ax.clear()

        self.ax.set_xlim([-13, 13])
        self.ax.set_ylim([-13, 13])
        self.ax.set_zlim([-13, 13])
        self.ax.set_title("3D Acceleration")

        self.counter = round(self.counter,1)
        print(self.counter)

        if self.counter < self.accela:
            self.counter += self.value
        elif self.counter > self.accela:
            self.counter -= self.value

        accel = np.array([self.counter,self.counter,0])
        origin= np.array([0,0,0])

        self.ax.quiver(*origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3)
        self.draw()


def get_float_input(    
    prompt: str, 
    default: float
    ) -> float:
    """
    Gets the input from the user using the terminal.

    Prompts the user to enter the angle for azimuth, declination, rotation, elevation, and bank.

    Args:
        prompt (str) : The desired question for the user to indicate which angle is required.
        default (float) : The default value of the angle if the user does not enter a value.
        
    Return: 
        float: the parsed string as float is returned

    Raises:
        ValueError: If the user's input is not a numerical value.
    """


    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ") or default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



def main()-> None:
    """
    This is the main function that executes the program.
    
    This function uses argparse to handle input from the command line.
    It creates an instance of the Compass class and sets its values using the inputs provided.
    
    Command-line arguments
    ----------------------
    -a : float
        Azimuth angle towards the desired location.
    -d : float
        Declination angle from the real north to the magnetic north.
    -b : float
        Bank angle at the longitudinal and horizontal axis.
    
    Examples:
        >>> python3 cli.py -a 45 -d 20 -b 2
    """


    parser = ArgumentParser(description="dmcview Command Line Interface")



    parser.add_argument(
        '-a',
        help= 'direction measured in degrees clockwise from north',
        type= float,
        default=None,
        nargs='?',
        metavar='azimuth'
    )
    parser.add_argument(
        '-d',
        help='difference between real north and magnetic north',
        type=float, 
        nargs='?',
        default=None,
        metavar='declination'
    )
    parser.add_argument(
        '-b',
        help='Inclination angle at the longitudinal and horizontal axis',
        type=float,
        nargs='?',
        default=None, 
        metavar='bank'
    )
    parser.add_argument(
        '-e',
        help='angular height of a point of interest above or below the horizon, in degrees',
        type=float,
        nargs='?',
        default=None, 
        metavar='bank'
    )
    

    args : Namespace = parser.parse_args()

    azimuth: float = args.a if args.a is not None else get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) # azimuth
    declination: float = args.d if args.d is not None else get_float_input("Enter the declination angle in degrees; for example 30.0", 0.0) # declination
    bank: float = args.b if args.b is not None else get_float_input("Enter the bank angle in degrees; for example -7.0", 0.0) # Inclination
    elevation: float = args.e if args.e is not None else get_float_input("Enter the elevation in degrees; for example 25.21",0.0) # elevation

    app = QApplication()

    main_widget = QWidget()

    layout = QHBoxLayout(main_widget)

    compass = Compass()
    layout.addWidget(compass)

    canvas = Accelaration_3D()
    canvas.setFixedSize(350,350)
    layout.addWidget(canvas)

    compass.update_declination(declination)  # This is Declination and can be float to two decimal places for example 35.55
    compass.update_angle(azimuth)  # This is Azimuth and can be float to two decimal places for example 35.55
    compass.set_rotation(bank) # This is the Inclination can be floated to two decimal places for example 35.55
    compass.set_elevation(elevation) # This is the Elevation can be floated to two decimal places for example 25.55
    

    timer = QTimer()
    timer.timeout.connect(canvas.update_plot)
    timer.start(10)  # Update every 100m

    main_widget.show()

    app.exec()

if __name__ == "__main__": # this is important so that it does not run from pytest 
    main()

