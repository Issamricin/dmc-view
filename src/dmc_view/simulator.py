from compass import Compass

class Simulator():
  
  def __init__(self)-> None:
        pass
  def run(self)->None:
      while True:
          print("Hi...\n")

def main()->None:
   sim = Simulator()
   sim.run()
 

if __name__ == "__main__": # this is import so that it does not run from pytest
    main()
