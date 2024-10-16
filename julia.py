import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


class Julia:

    def __init__(self, config):
        self.conf = config
        self.x_start = config["x_start"]
        self.y_start = config["y_start"]
        self.width = self.conf["width"]
        self.height = self.conf["height"]
        self.init_r = self.conf["init_r"]
        self.density = self.conf["density"]
        self.threshold = self.conf["threshold"]
        self.interval = self.conf["interval"]
        self.frames = self.conf["frames"]


    def julia_quadratic(self, zx, zy, cx, cy, threshold):
        """Calculates whether the number z[0] = zx + i*zy with a constant c = x + i*y
        belongs to the Julia set. In order to belong, the sequence
        z[i + 1] = z[i]**2 + c, must not diverge after 'threshold' number of steps.
        The sequence diverges if the absolute value of z[i+1] is greater than 4.

        :param float zx: the x component of z[0]
        :param float zy: the y component of z[0]
        :param float cx: the x component of the constant c
        :param float cy: the y component of the constant c
        :param int threshold: the number of iterations to considered it converged

        Code from:
        https://matplotlib.org/matplotblog/posts/animated-fractals/
        """
        # initial conditions
        z = complex(zx, zy)
        c = complex(cx, cy)

        traveled = 0
        for i in range(threshold):
            z = z ** 2 + c
            traveled += abs(z)
            if abs(z) > 4.:  # it diverged
                return i
        return threshold - 1  # it didn't diverge


    def animate(self, i):
        print(f"Processing frame {i}")

        # clear axes object and ticks
        self.ax.clear()
        self.ax.set_xticks([], [])
        self.ax.set_yticks([], [])

        # the initial array-like image
        X = np.empty((len(self.re), len(self.im)))

        # the initial c number
        cx = self.init_r * np.cos(self.a[i])
        cy = self.init_r * np.sin(self.a[i])

        # iterations for the given threshold
        for i in range(len(self.re)):
            for j in range(len(self.im)):
                X[i, j] = self.julia_quadratic(self.re[i], self.im[j], cx, cy, self.threshold)

        img = self.ax.imshow(X.T, interpolation="bicubic", cmap='magma')
        return [img]

    def generate(self):
        start = time.time()

        # real and imaginary axis
        self.re = np.linspace(
            self.x_start,
            self.x_start + self.width,
            self.width * self.density
        )
        self.im = np.linspace(
            self.y_start,
            self.y_start + self.height,
            self.height * self.density
        )

        self.a = np.linspace(0, 2 * np.pi, self.frames)

        self.fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
        self.ax = plt.axes()  # create an axes object

        anim = animation.FuncAnimation(
            self.fig,
            self.animate,
            frames=self.frames,
            interval=self.interval,
            blit=True
        )
        anim.save(self.conf["filename"], writer='imagemagick')

        print(f'{self.conf["frames"]} frames took {int((time.time()-start))} seconds')


Julia(
    {
        "x_start": -2,      # an interesting region starts here
        "y_start": -2,      # an interesting region starts here
        "width": 4,         # for 4 units up and right
        "height": 4,        # for 4 units up and right
        "init_r": 0.7885,   # we represent c as c = r*cos(a) + i*r*sin(a) = r*e^{i*a}
        "density": 500,     # more detail (200 is decent)
        "threshold": 50,    # more detail (20 is decent)
        "interval": 40,     # ms between frames
        "frames": 100,
        "filename": "julia_set.gif"
    }
).generate()
