import numpy as np
import quaternion

class transformation_data:
    def __init__(self):
        self.quaternion = quaternion.one
        self.translation = np.zeros((1,3))
        self.error = 0.0
    
    def as_transform_matrix(self):
        return np.vstack((np.hstack((quaternion.as_rotation_matrix(self.quaternion), self.translation.T)), np.array([0., 0., 0., 1.])))

class handle_data:
    Valid = 0x01
    Missing = 0x02
    Disabled = 0x03 

    def __init__(self):
        self.status = handle_data.Disabled
        self.transformation_data = transformation_data()
        self.port_status = 0
        self.frame_number = 0

if __name__ == "__main__":
    import math
    t = transformation_data()
    t.quaternion = quaternion.from_rotation_vector(math.radians(30.)  * np.array([0., 0., 1.]))
    t.translation = np.array([[1., 2., 3.]])
    print(t.as_transform_matrix())
