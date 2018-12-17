from numpy import full


class Canvas:
    def __init__(self, radius):
        self.radius = radius
        self.width = 2 * radius
        self.height = 2 * radius

        self.o_x = 256
        self.o_y = -256
        self.o_z = 320

        self.v_x = 0
        self.v_y = 0
        self.v_z = 640

    def get_image(self, material_tuple, lighting, spotlight):

        points = full((self.width, self.height, 1), 1.0)
        for i_x in range(self.width):
            for i_y in range(self.height):
                x = i_x - self.radius
                y = -i_y + self.radius
                if x ** 2 + y ** 2 > self.radius ** 2:
                    continue

                z = (self.radius ** 2 - x ** 2 - y ** 2) ** .5

                vector_n = [*map(lambda a: a / self.radius, [x, y, z])]

                l_x = self.o_x - x
                l_y = self.o_y - y
                l_z = self.o_z - z
                l_l = (l_x ** 2 + l_y ** 2 + l_z ** 2) ** .5
                vector_l = [*map(lambda a: a / l_l, [l_x, l_y, l_z])]

                v_x = self.v_x - x
                v_y = self.v_y - y
                v_z = self.v_z - z
                v_l = (v_x ** 2 + v_y ** 2 + v_z ** 2) ** .5
                vector_v = [*map(lambda a: a / v_l, [v_x, v_y, v_z])]

                n_l = vector_n[0] * vector_l[0] + vector_n[1] * vector_l[1] + vector_n[2] * vector_l[2]

                vector_r = [
                    vector_l[0] - 2 * (vector_n[0] * n_l),
                    vector_l[1] - 2 * (vector_n[1] * n_l),
                    vector_l[2] - 2 * (vector_n[2] * n_l),
                ]

                r_v = vector_r[0] * vector_v[0] + vector_r[1] * vector_v[1] + vector_r[2] * vector_v[2]

                points[i_x][i_y] = \
                    (lighting * material_tuple[1] + spotlight * ( material_tuple[2] * n_l + material_tuple[3] * r_v ** material_tuple[4]))

        return points


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_normalized_vector(self, x, y, z):
        vector_x = x - self.x
        vector_y = y - self.y
        vector_z = z - self.z

        vector_len = (vector_x ** 2 + vector_y ** 2 + vector_z ** 2) ** .5

        return Point(vector_x / vector_len, vector_y / vector_len, vector_z / vector_len)
