from compass import Compass
from PySide6.QtWidgets import QApplication
from argparse import ArgumentParser , Namespace


def get_float_input(
    prompt: str, 
    default: float
    ) -> float:

    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ") or default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")



def main():

    parser = ArgumentParser()

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
    

    args : Namespace = parser.parse_args()

    azimuth: float = args.a if args.a is not None else get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) # azimuth
    declination: float = args.d if args.d is not None else get_float_input("Enter the declination angle in degrees; for example 30.0", 0.0) # declination

    app = QApplication()
    compass = Compass()
    compass.show()
    compass.update_declination(declination)  #
    compass.update_angle(
        azimuth
    )  # This is Azimuth and can be float to two decimal places for example 35.55
    app.exec()


main()
