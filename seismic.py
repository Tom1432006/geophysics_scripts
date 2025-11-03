import math
from enum import Enum

angle = 10*math.pi/180 # in radiance

class Wave(Enum):
    P = 0
    S = 1

# [p-vel, s-vel, density, thickness]
layer_1 = [3.4*10**3, 2.9*10**3, 3.7*10**3, 10]
layer_2 = [3.9*10**3, 3.0*10**3, 3.9*10**3, 5]
layer_3 = [4.6*10**3, 3.5*10**3, 4.5*10**3, 12]

layers = [layer_1, layer_2, layer_3]

def calculate_reflection_coefficient(current_layer : int, wave : int, angle_i=0, angle_r=0) -> float:
    # R = (p2*v2*cosr-p1*v1*cosi)/(p2*v2*cosr+p1*v1*cosi)
    return ((layers[current_layer+1][2] * layers[current_layer+1][wave] * math.cos(angle_r) - layers[current_layer][2] * layers[current_layer][wave] * math.cos(angle_i))
            /
            (layers[current_layer+1][2] * layers[current_layer+1][wave] * math.cos(angle_r) + layers[current_layer][2] * layers[current_layer][wave] * math.cos(angle_i)))

def reflect(angle : int, aim_layer : int, wave : int, current_layer=0):
    if aim_layer == current_layer: return angle

    # refract at the current layer
    new_angle : float = math.asin(layers[current_layer+1][wave]*math.sin(angle)/layers[current_layer][wave])

    return reflect(new_angle, aim_layer, wave, current_layer+1)
    

def refract(angle : float, aim_layer : int, wave : int, current_layer=0) -> float:
    if current_layer == len(layers)-1: return 0
    new_angle : float = math.asin(layers[current_layer+1][wave]*math.sin(angle)/layers[current_layer][wave])
    if aim_layer == current_layer: return new_angle

    return refract(new_angle, aim_layer, wave, current_layer+1)


if __name__ == "__main__":
    for i in range(0,3):
        print("reflect layer " + str(i+1) + ";      P-Wave: Angle: " + str((180*reflect(angle, i, Wave.P.value)/math.pi)) + "°")
        print("reflect layer " + str(i+1) + ";      S-Wave: Angle: " + str((180*reflect(angle, i, Wave.S.value)/math.pi)) + "°")

        if i != 2:
            print("refract layer " + str(i+1) + " to " +  str(i+2) + "; P-Wave: Angle: " + str((180*refract(angle, i, Wave.P.value)/math.pi)) + "°")
            print("refract layer " + str(i+1) + " to " +  str(i+2) + "; S-Wave: Angle: " + str((180*refract(angle, i, Wave.S.value)/math.pi)) + "°")

    print()
    print()

    print("Reflection coeficcient P-Wave: " + str(calculate_reflection_coefficient(1, Wave.P.value)))
    print("Reflection coeficcient S-Wave: " + str(calculate_reflection_coefficient(1, Wave.S.value)))