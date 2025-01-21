import time
from random import uniform

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication

from dmcview.compass import Compass


class SimulatorSignal(QObject):
      '''Define the signals available from a running worker thread'''
      result= Signal(str,str,str) # azimuth, elevation and bank


class SimulatorRunner(QRunnable):
    
    def __init__(self) -> None:
        super().__init__()
        self.signal = SimulatorSignal()
      
    @Slot()
    def run(self)-> None:
        while True:
            azimuth = round(uniform(20.0,40.0),2)
            inclination = round(uniform(20.0,35.0),2)
            bank = round(uniform(30.0, 45.0),2)
            print("Azimuth:{0}; Inclination(Elevation):{1}; Bank(Rotation):{2}".format(azimuth,inclination,bank))
            self.signal.result.emit(str(azimuth), str(inclination),str(bank))
            time.sleep(2)# two seconds
    
    
class Simulator():
  
  def __init__(self)-> None:
        self.threadPool = QThreadPool()
        self.runner = SimulatorRunner()
        
  def run(self)->None:
      self.runner.signal.result.connect(self.__update)
      self.threadPool.start(self.runner)
      app = QApplication()
      self.compass = Compass()
      self.compass.show()
      self.compass.update_declination(10.5)
      self.compass.update_angle(39.5)
      self.compass.set_rotation(30.0)
      self.compass.set_elevation(35.5)                 
      app.exec()
     
  def __update(self,azimuth:str, elevation:str, bank:str)->None: 
        self.compass.update_angle(float(azimuth))
        self.compass.set_elevation(float(elevation))
        self.compass.set_rotation(float(bank))
        
        
          
  
def main()->None:
   sim = Simulator()
   sim.run()
 

if __name__ == "__main__": # this is import so that it does not run from pytest
    main()
