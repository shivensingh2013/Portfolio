# --TODO-- Quart to angles to be checked and fixed

## Function to convert Quartenion to Pitch,Yaw and Roll (Euler angle) system
import math
def quart_to_angles(rotation) -> tuple:
    """
    Compute yaw-pitch-roll Euler angles from a quaternion.
    
    Args
    ----
        q0: Scalar component of quaternion.
        q1, q2, q3: Vector components of quaternion.
    
    Returns
    -------
        (roll, pitch, yaw) (tuple): 321 Euler angles in radians
    """
    q0 = rotation[0]
    q1 = rotation[1]
    q2 = rotation[2]
    q3 = rotation[3]
    
    roll = math.atan2(2 * ((q2 * q3) + (q0 * q1)),q0**2 - q1**2 - q2**2 + q3**2 )  # radians
    pitch = math.asin(2 * ((q1 * q3) - (q0 * q2)))
    yaw = math.atan2( 2 * ((q1 * q2) + (q0 * q3)),q0**2 + q1**2 - q2**2 - q3**2)

    roll = roll* (180 / math.pi)
    pitch= pitch* (180 / math.pi)
    yaw = yaw* (180 / math.pi)
    return (yaw, pitch, roll)

