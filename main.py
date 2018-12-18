import cv2

from geometry import Canvas

materials = (
    {'name': 'Metal', 'ka': 0.1, 'kd': 0.4, 'ks': 0.6, 'n': 101.0},
    {'name': 'Wood', 'ka': 0.5, 'kd': 0.6, 'ks': 0.4, 'n': 11.0},
    {'name': 'Chalk', 'ka': 0.8, 'kd': 0.9, 'ks': 0.01, 'n': 26.0},
    {'name': 'Plastic', 'ka': 0.45, 'kd': 0.9, 'ks': 0.2, 'n': 51.0},
)


def main():
    canvas = Canvas(128)
    material_i = 0
    lighting = 0.1
    spotlight = 1.0

    while True:
        cv2.imshow(
            'Phong Shading',
            canvas.get_image(materials[material_i], lighting, spotlight)
        )
        k = cv2.waitKey(0)

        if k == 83:
            material_i += 1
            material_i %= len(materials)
        elif k == 81:
            material_i -= 1
            material_i %= len(materials)
        elif k == 82:
            lighting += 0.1
        elif k == 84:
            lighting -= 0.1
        elif k == ord('-'):
            spotlight -= 0.1
        elif k == ord('+'):
            spotlight += 0.1


if __name__ == '__main__':
    main()
