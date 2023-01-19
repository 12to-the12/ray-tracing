
import numpy as np
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
from ignore import ignore
from clear_terminal import clear_terminal
from alert import alert


class Camera():
    def __init__(self):
        pass
    def __str__(self) -> str:
        return f"camera view_vector: {self.view_vector}"
    def translate(self,change):
        assert change.shape == (3), f"change should be an array with three elements, not {change.shape}"
        self.position = self.position + change


    def orient(self):
        """this function returns the pair of axes and angles
        necessary to rotate the camera's position towards -Z, +Y
        these can be used to apply the inverse to vertexes in the scene
        to make them rotate relative to the camera"""
        Z   = np.array([ 0., 0., 1.]) #  Z
        n_Z = np.array([ 0., 0.,-1.]) # -Z
        Y   = np.array([ 0., 1., 0.]) # +Y
        X   = np.array([ 1., 0., 0.]) # +X

        


        angle_a = angle(self.view_vector,n_Z)

        if angle_a == 180:
            intermediary_up   = arbitrary_axis_rotation(self.up_vector,  X,180)
        elif angle_a: # only necessary if angle_a is non zero
            axis_a = orthogonal(self.view_vector,n_Z) # computed axis of rotation
            # intermediary is the result of applying the operation that aligns the
            # view vector with -Z to the up vector
            intermediary_up   = arbitrary_axis_rotation(self.up_vector,  axis_a,angle_a)
        else:
            axis_a = n_Z 


        # the next step is to align the up vector with +Y

        angle_b = angle(intermediary_up,Y)

        if angle_b == 180:
            axis_b = n_Z
        elif angle_b: # only necessary if angle_a is non zero
            axis_b = orthogonal(intermediary_up,Y) # computed axis of rotation
            # intermediary is the result of applying the operation that aligns the
            # view vector with -Z to the up vector
        else:
            axis_b = n_Z

        return [axis_a,angle_a,axis_b,angle_b]
        alert(f"angle a:\t{angle_a}")
        alert(f" axis a:\t{axis_a}")

        alert(f"angle b:\t{angle_b}")
        alert(f" axis b:\t{axis_b}")


        intermediary_view = arbitrary_axis_rotation(self.view_vector,axis_a,angle_a)
        alert(f"intermediary view: {intermediary_view}")
        alert(f"intermediary up: {intermediary_up}")
        final_view = arbitrary_axis_rotation(intermediary_view,axis_b,angle_b)
        final_up   = arbitrary_axis_rotation(intermediary_up,  axis_b,angle_b)
        alert(f"final view: {final_view}")
        alert(f"final up:   {final_up}")
        intermediary_view = arbitrary_axis_rotation(final_view,axis_b,-angle_b)
        intermediary_up   = arbitrary_axis_rotation(final_up,  axis_b,-angle_b)
        alert(f"intermediary view: {intermediary_view}")
        alert(f"intermediary up: {intermediary_up}")
        output_view = arbitrary_axis_rotation(intermediary_view,axis_a,-angle_a)
        output_up   = arbitrary_axis_rotation(intermediary_up,  axis_a,-angle_a)
        alert()
        alert(f"output view:  \t{output_view}")
        alert(f"starting view:\t{self.view_vector}")
        alert()
        alert(f"output up:    \t{output_up}")
        alert(f"starting up:  \t{self.up_vector}")
        alert()

        



    # these rotations operate in camera space
    # assuming the vector is pointing towards you, 
    # counter clockwise is the positive direction of rotation
    def rotate_pitch(self,degrees):
        # y and z, x is the vector
        # nodding, upwards nod is positive
        
        cross = np.cross(self.view_vector,self.up_vector)
        self.up_vector   = arbitrary_axis_rotation(self.up_vector, cross, degrees)
        self.view_vector = arbitrary_axis_rotation(self.view_vector, cross, degrees)
        
    def rotate_yaw(self,degrees):
        # x and y, z is the vector
        # shaking head, left rotation is positive
        self.view_vector = arbitrary_axis_rotation(self.view_vector, self.up_vector, degrees)
    def rotate_roll(self,degrees):
        # x and z, y is the vector
        # side to side, indian head nod, rolling right is positive
        self.up_vector = arbitrary_axis_rotation(self.up_vector, self.view_vector, degrees)
    

if __name__ == "__main__":
    np.set_printoptions(suppress=True) # suppresses scientific notation
    clear_terminal()
    camera = Camera()
    camera.position    = np.array(( 0,-1, 0)) # x,y,z
    camera.view_vector = np.array(( 0, 1, 0))
    camera.up_vector   = np.array(( 0, 0, 1))

    

    

    for x in [-180,0,180,360,50]:
        camera.rotate_yaw(x) # left
        camera.rotate_pitch(x) # up
        camera.rotate_roll(x) # up

        camera.orient()