from dmc_view.compass import Compass
from PySide6.QtWidgets import QApplication
from argparse import ArgumentParser , Namespace


def get_float_input(
    prompt: str, 
    default: float
    ) -> float:
    """
    Gets the input from the user using the terminal.

    Prompts the user to enter the angle for azimuth, declination, rotation, and bank.

    Parameters
    ----------
    prompt : str
        The desired question for the user to indicate which angle is required.
    default : float
        The default value of the angle if the user does not enter a value.

    Raises
    ------
    ValueError
        If the user's input is not a numerical value.
    """


    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ") or default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



def main():
    """This is the main function that executes the program.

    This function uses argparse to handle input from the command line.
    It create an instance of Compass class and sets its values using the inputs provided.
    
    Command-line arguments
    ----------------------
    -a : float
        Azimuth angle towards the desired location.
    -d : float
        Declination angle from the real north to the magnatic north.
    -b : float
        Bank angle at the longitudinal and horizontal axis.

    Examples
    --------
    >>>python3 main.py -a 45 -d 20 -b 2
    """

    parser = ArgumentParser(description="DMC_view Command Line Interface")



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
    

    args : Namespace = parser.parse_args()

    azimuth: float = args.a if args.a is not None else get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) # azimuth
    declination: float = args.d if args.d is not None else get_float_input("Enter the declination angle in degrees; for example 30.0", 0.0) # declination
    bank: float = args.b if args.b is not None else get_float_input("Enter the bank angle in degrees; for example -7.0", 0.0) # Inclination


    app = QApplication()
    compass = Compass()
    compass.show()

    compass.update_declination(declination)  # This is Declination and can be float to two decimal places for example 35.55
    compass.update_angle(azimuth)  # This is Azimuth and can be float to two decimal places for example 35.55
    compass.set_rotation(bank) # This is the Inclination can be floated to two decimal places for example 35.55

    app.exec()

if __name__ == "__main__": # this is important so that it does not run from pytest 
    main()
