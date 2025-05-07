import pygame
import math
import sys
import serial
import time
import re

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255); RED = (255, 0, 0); GREEN = (0, 255, 0)
BLUE = (0, 0, 255); BLACK = (0, 0, 0); YELLOW = (255, 255, 0)
CYAN = (0, 255, 255); MAGENTA = (255, 0, 255)

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 0.01

FOCAL_LENGTH = 350
VIEWER_DISTANCE = 6
SCALE = 120

COMPLEMENTARY_FILTER_ALPHA = 0.98
INVERT_PITCH = False
INVERT_ROLL = False
INVERT_YAW = False

points = []
points.append((-0.3, 0.0, -0.3)); points.append(( 0.3, 0.0, -0.3)) # 0, 1
points.append(( 0.3, 0.0,  0.3)); points.append((-0.3, 0.0,  0.3)) # 2, 3
arm_y = 0.05; prop_dist = 0.7
points.append(( prop_dist, arm_y, -prop_dist)); points.append((-prop_dist, arm_y, -prop_dist))
points.append((-prop_dist, arm_y,  prop_dist)); points.append(( prop_dist, arm_y,  prop_dist))
prop_y = 0.1; prop_size = 0.15
px, py, pz = points[4]; points.extend([(px - prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz + prop_size), (px - prop_size, prop_y, pz + prop_size)])
px, py, pz = points[5]; points.extend([(px - prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz + prop_size), (px - prop_size, prop_y, pz + prop_size)])
px, py, pz = points[6]; points.extend([(px - prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz + prop_size), (px - prop_size, prop_y, pz + prop_size)])
px, py, pz = points[7]; points.extend([(px - prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz - prop_size), (px + prop_size, prop_y, pz + prop_size), (px - prop_size, prop_y, pz + prop_size)])

edges = []
edges.extend([(0, 1), (1, 2), (2, 3), (3, 0)])
edges.extend([(1, 4), (0, 5), (3, 6), (2, 7)])
edges.extend([(4, 9), (5, 13), (6, 17), (7, 21)])
edges.extend([(8, 9), (9, 10), (10, 11), (11, 8)])
edges.extend([(12, 13), (13, 14), (14, 15), (15, 12)])
edges.extend([(16, 17), (17, 18), (18, 19), (19, 16)])
edges.extend([(20, 21), (21, 22), (22, 23), (23, 20)])

axis_points = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2)]
axis_edges = [(0, 1), (0, 2), (0, 3)]
axis_colors = [BLUE,RED , GREEN]
axis_labels = ["Z", "X", "Y"]

CARDINAL_DISTANCE = 3.0
cardinal_labels = ["N", "S", "E", "W"]
cardinal_points = [
    (0, 0, CARDINAL_DISTANCE),
    (0, 0, -CARDINAL_DISTANCE),
    (CARDINAL_DISTANCE, 0, 0),
    (-CARDINAL_DISTANCE, 0, 0)
]
cardinal_color = YELLOW

def rotate_point(x, y, z, angle_x, angle_y, angle_z):
    rad_x = angle_x; y_new = y * math.cos(rad_x) - z * math.sin(rad_x); z_new = y * math.sin(rad_x) + z * math.cos(rad_x); y, z = y_new, z_new
    rad_y = angle_y; x_new = x * math.cos(rad_y) + z * math.sin(rad_y); z_new = -x * math.sin(rad_y) + z * math.cos(rad_y); x, z = x_new, z_new
    rad_z = angle_z; x_new = x * math.cos(rad_z) - y * math.sin(rad_z); y_new = x * math.sin(rad_z) + y * math.cos(rad_z); x, y = x_new, y_new
    return x, y, z

def project_point(x, y, z):
    x *= SCALE; y *= SCALE; z *= SCALE
    z_adjusted = z + VIEWER_DISTANCE * SCALE
    if z_adjusted <= FOCAL_LENGTH * 0.1: return None
    factor = FOCAL_LENGTH / z_adjusted
    screen_x = int(x * factor + WIDTH / 2)
    screen_y = int(-y * factor + HEIGHT / 2)
    return (screen_x, screen_y)

data_pattern = re.compile(r"(\w+)\s+X:\s*(-?[\d.]+),\s*Y:\s*(-?[\d.]+),\s*Z:\s*(-?[\d.]+)")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Pygame 3D Drone - MPU6050 ({SERIAL_PORT})")
clock = pygame.time.Clock()
try:
    main_font = pygame.font.SysFont('Arial', 18, bold=True)
except:
    print("Arial font not found, using default Pygame font.")
    main_font = pygame.font.Font(None, 24)

ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
    print(f"Successfully opened serial port {SERIAL_PORT}")
    time.sleep(1); ser.flushInput()
except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    print("Running visualization without MPU data.")

pitch = 0.0; roll = 0.0; yaw = 0.0
angle_x = 0.0; angle_y = 0.0; angle_z = 0.0

current_accel = [0.0, 0.0, 0.0]; current_gyro = [0.0, 0.0, 0.0]
last_update_time = time.time()

running = True
while running:
    dt = clock.tick(60) / 1000.0
    if dt == 0: dt = 1/60.0

    if ser and ser.is_open:
        try:
            while ser.in_waiting > 0:
                line = ser.readline()
                if not line: continue
                try:
                    decoded_line = line.decode('utf-8', errors='ignore').strip()
                    match = data_pattern.match(decoded_line)
                    if match:
                        data_type, x_str, y_str, z_str = match.groups()
                        x, y, z = float(x_str), float(y_str), float(z_str)
                        if data_type == "Accel":
                            current_accel = [x, y, z]
                        elif data_type == "Gyro":
                            current_gyro = [math.radians(g) for g in [x, y, z]]
                except Exception as e:
                    pass 
        except serial.SerialException as se:
            print(f"Serial error: {se}. Closing port."); ser.close(); ser = None
        except OSError as ose:
             print(f"OS error reading serial: {ose}. Closing port."); ser.close(); ser = None

    acc_x, acc_y, acc_z = current_accel
    if not (acc_x == 0 and acc_y == 0 and acc_z == 0):
        accel_roll_denom = math.sqrt(acc_x**2 + acc_z**2)
        accel_pitch_denom = math.sqrt(acc_y**2 + acc_z**2)

        accel_roll = math.atan2(acc_y, accel_roll_denom) if accel_roll_denom > 1e-6 else 0.0
        accel_pitch = math.atan2(-acc_x, accel_pitch_denom) if accel_pitch_denom > 1e-6 else 0.0

        gyro_x, gyro_y, gyro_z = current_gyro
        pitch = COMPLEMENTARY_FILTER_ALPHA * (pitch + gyro_x * dt) + (1 - COMPLEMENTARY_FILTER_ALPHA) * accel_pitch
        roll = COMPLEMENTARY_FILTER_ALPHA * (roll + gyro_y * dt) + (1 - COMPLEMENTARY_FILTER_ALPHA) * accel_roll
        yaw = yaw + gyro_z * dt # Yaw drifts

    angle_x = roll  * (-1 if INVERT_ROLL else 1)
    angle_y = yaw   * (-1 if INVERT_YAW else 1)
    angle_z = pitch * (-1 if INVERT_PITCH else 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
             if event.button == 4: SCALE += 10
             elif event.button == 5: SCALE = max(20, SCALE - 10)

    projected_points = [project_point(*rotate_point(*p, angle_x, angle_y, angle_z)) for p in points]
    projected_axis_points = [project_point(*rotate_point(*p, angle_x, angle_y, angle_z)) for p in axis_points]
    projected_cardinal_points = [project_point(*rotate_point(*p, angle_x, angle_y, angle_z)) for p in cardinal_points]

    screen.fill(BLACK)

    origin_proj = projected_axis_points[0]
    if origin_proj:
        for i, edge in enumerate(axis_edges):
             p1_idx, p2_idx = edge
             if 0 <= p1_idx < len(projected_axis_points) and 0 <= p2_idx < len(projected_axis_points):
                 p1_proj = projected_axis_points[p1_idx]; p2_proj = projected_axis_points[p2_idx]
                 if p1_proj and p2_proj:
                     pygame.draw.line(screen, axis_colors[i], p1_proj, p2_proj, 2)
        pygame.draw.circle(screen, WHITE, origin_proj, 4)
    label_offset = 15
    for i in range(3):
        axis_end_index = i + 1
        if 0 <= axis_end_index < len(projected_axis_points):
            proj_end = projected_axis_points[axis_end_index]
            if proj_end:
                label_text = axis_labels[i]; label_color = axis_colors[i]
                text_surface = main_font.render(label_text, True, label_color)
                text_rect = text_surface.get_rect()
                label_pos_x, label_pos_y = proj_end[0], proj_end[1]
                if origin_proj:
                    dx = proj_end[0] - origin_proj[0]; dy = proj_end[1] - origin_proj[1]
                    dist = math.hypot(dx, dy)
                    if dist > 1e-5:
                        label_pos_x = proj_end[0] + (dx / dist) * label_offset
                        label_pos_y = proj_end[1] + (dy / dist) * label_offset
                text_rect.center = (int(label_pos_x), int(label_pos_y))
                screen.blit(text_surface, text_rect)

    for i, proj_cp in enumerate(projected_cardinal_points):
        if proj_cp:
            label_text = cardinal_labels[i]
            text_surface = main_font.render(label_text, True, cardinal_color)
            text_rect = text_surface.get_rect(center=proj_cp)

            screen.blit(text_surface, text_rect)


    for edge in edges:
        p1_idx, p2_idx = edge
        if 0 <= p1_idx < len(projected_points) and 0 <= p2_idx < len(projected_points):
            p1_proj = projected_points[p1_idx]; p2_proj = projected_points[p2_idx]
            if p1_proj and p2_proj:
                pygame.draw.line(screen, CYAN, p1_proj, p2_proj, 1)

    pygame.display.flip()

if ser and ser.is_open: ser.close(); print(f"Closed serial port {SERIAL_PORT}")
pygame.quit()
sys.exit()
