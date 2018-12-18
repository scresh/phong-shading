from numpy import full
import cv2


class Canvas:
    def __init__(self, radius):
        self.radius = radius
        self.width = 2 * radius
        self.height = 2 * radius

        # Source of light
        self.l_x = 720
        self.l_y = -720
        self.l_z = 320

        # Observer
        self.v_x = 0
        self.v_y = 0
        self.v_z = 640

        self.n_l = full((self.width, self.height, 1), 0.0)
        self.r_v = full((self.width, self.height, 1), 0.0)

        # Calculate vector scalar products for each hemisphere point (N o L) and (R o V)
        for i_x in range(self.width):
            for i_y in range(self.height):

                # Real position
                x = i_x - self.radius
                y = -i_y + self.radius

                # Check if point inside circle
                if x ** 2 + y ** 2 > self.radius ** 2:
                    continue

                z = (self.radius ** 2 - x ** 2 - y ** 2) ** 0.5

                vector_n = [*map(lambda l: (l / self.radius), [x, y, z])]

                l_x = self.l_x - x
                l_y = self.l_y - y
                l_z = self.l_z - z
                l_l = (l_x ** 2 + l_y ** 2 + l_z ** 2) ** 0.5
                vector_l = [*map(lambda l: (l / l_l), [l_x, l_y, l_z])]

                v_x = self.v_x - x
                v_y = self.v_y - y
                v_z = self.v_z - z
                v_l = (v_x ** 2 + v_y ** 2 + v_z ** 2) ** 0.5
                vector_v = [*map(lambda l: (l / v_l), [v_x, v_y, v_z])]

                self.n_l[i_x][i_y] = vector_n[0] * vector_l[0] + vector_n[1] * vector_l[1] + vector_n[2] * vector_l[2]

                r_x = 2 * (vector_n[0] * self.n_l[i_x][i_y]) - vector_l[0]
                r_y = 2 * (vector_n[1] * self.n_l[i_x][i_y]) - vector_l[1]
                r_z = 2 * (vector_n[2] * self.n_l[i_x][i_y]) - vector_l[2]
                r_l = (r_x ** 2 + r_y ** 2 + r_z ** 2) ** 0.5
                vector_r = [*map(lambda l: (l / r_l), [r_x, r_y, r_z])]

                self.r_v[i_x][i_y] = vector_r[0] * vector_v[0] + vector_r[1] * vector_v[1] + vector_r[2] * vector_v[2]

    def get_image(self, material_dict, ia, ii):
        points = full((self.width, self.height, 1), 1.0)

        name = material_dict['name']
        ka = material_dict['ka']
        kd = material_dict['kd']
        ks = material_dict['ks']
        n = material_dict['n']

        for i_x in range(self.width):
            for i_y in range(self.height):

                # Real position
                x = i_x - self.radius
                y = self.radius - i_y

                # Check if point inside circle
                if x ** 2 + y ** 2 > self.radius ** 2:
                    continue

                points[i_x][i_y] = ka * ia + ii * (kd * self.n_l[i_x][i_y] + ks * (self.r_v[i_x][i_y] ** n))

        cv2.putText(
            points,
            name,
            (int(self.width / 48), int(self.height / 24)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1 / 640 * self.width,
            (0, 0, 0),
            1
        )

        return points
