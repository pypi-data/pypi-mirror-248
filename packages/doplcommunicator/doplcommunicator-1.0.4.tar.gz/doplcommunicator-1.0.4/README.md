# Data Communicator Client

Sends and receives data between clients connected to Dopl

## Usage

```python
# Robot
from doplcommunicator import DoplCommunicator
from doplcommunicator.controllerdata import ControllerData

def on_joined_session(session_id: int):
    print('Joined session id', session_id)

def on_controller_data(controller_data: ControllerData):
    print('Controller data received', controller_data.toJSON())
    # Apply the controller data to the robot

communicator = DoplCommunicator("http://localhost:3000")
communicator.on_joined_session(on_joined_session)
communicator.on_controller_data(on_controller_data)
communicator.connect()
```

```python
# Robot Controller
import time
from doplcommunicator import DoplCommunicator
from doplcommunicator.controllerdata import ControllerData

def on_joined_session(session_id: int):
    print('Joined session id', session_id)

communicator = DoplCommunicator("http://localhost:3000")
communicator.on_joined_session(on_joined_session)
communicator.connect()

while(True):
    x = y = z = rx = ry = rz = rw = 0
    communicator.controller_data = ControllerData(x, y, z, rx, ry, rz, rw)
    time.sleep(0.01)
```