import time
from random import uniform

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from compass import Compass
from acceleration import Accelaration3D


class SimulatorSignal(QObject):
      '''Define the signals available from a running worker thread'''
      result= Signal(str,str,str,str,str,str) # azimuth, elevation, bank and acceleration (x,y,z)


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
            x = round(uniform(5.0,15.0),1)
            y = x
            z = 0.0

            print("Azimuth:{0}; Inclination(Elevation):{1}; Bank(Rotation):{2}; acceleration:{3}".format(azimuth,inclination,bank,[x,y,z]))
            self.signal.result.emit(str(azimuth), str(inclination),str(bank),str(x),str(y),str(z))
            QThread.sleep(2.5)# two seconds
    
    
class Simulator():
  
  def __init__(self)-> None:
        self.threadPool = QThreadPool()
        self.runner = SimulatorRunner()
        
  def run(self)->None:
      self.runner.signal.result.connect(self.__update)
      self.threadPool.start(self.runner)
     
      app = QApplication()
      main_widget = QWidget()
      layout = QHBoxLayout(main_widget)
      self.compass = Compass()
  
      layout.addWidget(self.compass)
  
      self.canvas = Accelaration3D()
      self.canvas.setFixedSize(350,350)
      layout.addWidget(self.canvas)

      self.compass.update_declination(10.5)

      main_widget.show()               
      app.exec()
     
  def __update(self,azimuth:str, elevation:str, bank:str, x:str, y:str, z:str)->None: 
        self.compass.update_angle(float(azimuth))
        self.compass.set_elevation(float(elevation))
        self.compass.set_rotation(float(bank))
        self.canvas.update_acceleration(round(float(x),1),round(float(y),1),round(float(z),1))
        
        
          
  
def main()->None:
   sim = Simulator()
   sim.run()
 

if __name__ == "__main__": # this is import so that it does not run from pytest
    main()
