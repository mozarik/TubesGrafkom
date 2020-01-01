from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


x_min, y_min = 50, 50
x_max, y_max = 100, 100


nx_min, ny_min = 200, 200
nx_max, ny_max = 350, 350

t1, t2 = 0.0, 1.0  # Intial and final time

x1, y1 = 0, 0
# Point 1
x2, y2 = 100, 150
# Point 2


# void myDisplay();
# void draw_lineAndPort(double x1, double y1, double x2, double y2, double y_max, double y_min, double x_max, double x_min);
# void liangBarsky(double x1, double y1, double x2, double y2);
# bool cliptest(double p, double q);


def myInit():
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, 500, 0, 500)
    glMatrixMode(GL_MODELVIEW)


def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_lineAndPort(x1, y1, x2, y2, y_max, y_min, x_max, x_min)
    liangBarsky(x1, y1, x2, y2)

    glFlush()


def draw_lineAndPort(x1, y1, x2, y2, y_max, y_min, x_max, x_min):

    glColor3d(1, 0, 0)
    glBegin(GL_LINE_LOOP)
    glVertex2d(x_min, y_min)
    glVertex2d(x_max, y_min)
    glVertex2d(x_max, y_max)
    glVertex2d(x_min, y_max)
    glEnd()

    glColor3d(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2d(x1, y1)
    glVertex2d(x2, y2)
    glEnd()


def cliptest(p, q):
    t = q / p
    global t1, t2
    if p == 0 and q < 0:  # Line is parallel to viewport and outside
        return False

    elif p < 0:
        if t > t1:
            t1 = t
        if t > t2:
            return False

    elif p > 0:
        if t < t2:
            t2 = t
        if t < t1:
            return False
    return True


def liangBarsky(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    """
     -t * dx < x1 - x_min        ... [1]
      t * dx < x_max - x1        ... [2]
     -t * dy < y1 - y_min        ... [3]
      t * dy < y_max - y1        ... [4]
     """
    if (
        cliptest(-dx, x1 - x_min)
        and cliptest(dx, x_max - x1)
        and cliptest(-dy, y1 - y_min)
        and cliptest(dy, y_max - y1)
    ):
        if t2 < 1:
            x2 = x1 + t2 * dx
            y2 = y1 + t2 * dy
        if t1 > 0:
            x1 = x1 + t1 * dx
            y1 = y1 + t1 * dy

        # Scaling to new View port
        scale_x = (nx_max - nx_min) / (x_max - x_min)
        scale_y = (ny_max - ny_min) / (y_max - y_min)

        # Point pada kotak sebelum di Scaling (the real)
        # New coordinates of the points
        # Point 1
        nx1_real = x1 - x_min + 50
        ny1_real = y1 - y_min + 50

        # Point 2
        nx2_real = x2 - x_min + 50
        ny2_real = y2 - y_min + 50

        # Point pada Kotak yang sudah di Scaling
        # Point 1
        nx1 = nx_min + (x1 - x_min) * scale_x
        ny1 = ny_min + (y1 - y_min) * scale_y

        # Point 2
        nx2 = nx_min + (x2 - x_min) * scale_x
        ny2 = ny_min + (y2 - y_min) * scale_y

        # Plotting new Viewport and clipped line
        draw_lineAndPort(nx1, ny1, nx2, ny2, ny_max, ny_min, nx_max, nx_min)

        glPointSize(5)
        glColor3d(1, 5, 200)
        glBegin(GL_POINTS)
        glVertex2d(nx1, ny1)
        print(
            "Titik Bawah Berpotong Pada Atas x1 = {} dan y1 = {}".format(
                nx1_real, ny1_real
            )
        )
        glVertex2d(nx2, ny2)
        print(
            "Titik Bawah Berpotong Pada Atas x2 = {} dan y2 = {}".format(
                nx2_real, ny2_real
            )
        )
        glVertex2d(nx1_real, ny1_real)
        glVertex2d(nx2_real, ny2_real)
        glEnd()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE or GLUT_RGB)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(700, 700)

    glutCreateWindow("Liang Barsky")

    glutDisplayFunc(myDisplay)
    myInit()
    glutMainLoop()
    return 0


if __name__ == "__main__":
    main()
