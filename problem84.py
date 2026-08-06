#06/08/2026
#Medium
#Find Angle MBC
# HackerRank: Calculate the angle of a right triangle's median using trigonometry and math.atan2.
import math
ab = int(input())
bc = int(input())
angle_rad = math.atan2(ab, bc)
angle_deg = round(math.degrees(angle_rad))
print(f"{angle_deg}°")