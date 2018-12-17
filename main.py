import cv2

from geometry import Canvas

materials = (
    ('Metal', 0.1, 0.4, 0.6, 100.0),
    ('Wood', 0.5, 0.6, 0.4, 10.0),
    ('Chalk', 0.8, 0.9, 0.01, 25.0),
    ('Plastic', 0.045, 0.9, 0.2, 50.0),
)


def main():
    canvas = Canvas(128)
    material_i = 0
    lighting = 0.1
    spotlight = 1.0

    while True:
        cv2.imshow('asd', canvas.get_image(materials[material_i], lighting, spotlight))
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