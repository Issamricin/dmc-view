""" The command line interface (CLI) parser """
from argparse import ArgumentParser, Namespace

from compass import Compass

from acceleration import  Accelaration3D

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import QTimer


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

def get_acceleration_input(    
    prompt: str, 
    x: float,
    y: float,
    z: float
    ) -> float:

    while True:
        try:
            user_input = input(f"{prompt} (default {x,y,z}): ").split()
            try:
                user_x = user_input[0] 
            except IndexError:   
                user_x = x
            try:
                user_y = user_input[1]
            except IndexError:
                user_y = y
            try:
                user_z = user_input[2]
            except IndexError:
                user_z = z

            return float(user_x),float(user_y),float(user_z)
        
        except ValueError:
            print("Invalid input. Please enter a correct numeric value.")



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
        metavar='inclination'
    )
    parser.add_argument(
        '-e',
        help='angular height of a point of interest above or below the horizon, in degrees',
        type=float,
        nargs='?',
        default=None, 
        metavar='bank'
    )
    parser.add_argument(
        '-ac',
        help='acceleration of the object, using 3 points vector',
        type=float,
        nargs='?',
        default=None, 
        metavar='acceleration'
    )
    

    args : Namespace = parser.parse_args()

    azimuth: float = args.a if args.a is not None else get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) # azimuth
    declination: float = args.d if args.d is not None else get_float_input("Enter the declination angle in degrees; for example 30.0", 0.0) # declination
    bank: float = args.b if args.b is not None else get_float_input("Enter the bank angle in degrees; for example -7.0", 0.0) # Inclination
    elevation: float = args.e if args.e is not None else get_float_input("Enter the elevation in degrees; for example 25.21",0.0) # elevation
    x,y,z = args.ac if args.ac is not None else get_acceleration_input("Enter the acceleration values(vectors: x,y,z); for example 12 12 0",0,0,0)

    app = QApplication()
    main_widget = QWidget()
    layout = QHBoxLayout(main_widget)
    compass = Compass()

    layout.addWidget(compass)

    canvas = Accelaration3D()
    canvas.setFixedSize(350,350)
    layout.addWidget(canvas)


    #def on_resize(event):
    #    screen_size = main_widget.size()
    #    if screen_size.width()<1000 or screen_size.height()<500:
    #        canvas.setFixedSize(250,250)
    #    else:
    #        canvas.setFixedSize(350,350)
    #    
    #    print(screen_size)

    #main_widget.resizeEvent = on_resize

    compass.update_declination(declination)  # This is Declination and can be float to two decimal places for example 35.55
    compass.update_angle(azimuth)  # This is Azimuth and can be float to two decimal places for example 35.55
    compass.set_rotation(bank) # This is the Inclination can be floated to two decimal places for example 35.55
    compass.set_elevation(elevation) # This is the Elevation can be floated to two decimal places for example 25.55

    canvas.update_acceleration(x,y,z)

    main_widget.show()
    app.exec()

if __name__ == "__main__": # this is important so that it does not run from pytest 
    main()
