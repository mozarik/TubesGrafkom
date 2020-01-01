# Nama Anggota Kelompok

Nama  | NIM
------------ | -------------
Muhammad Zein I. F. | 201810370311072
Iqlima Chairunnisa | 	201810370311079
Lale Wiega A. C. | 	201810370311061
Sarlita Rizka A. | 201810370311075
Tanthowi Jauhari | 01810370311054

# Readme

Disini kami membuat sebuah program implementasi algoritma clipping Liang-Barsky menggunakan OpenGL, kami disini menggunakan Bahasa Pemrograman Python 3.7

# Dokumentasi

## Inisialisasi variabel


Kami menggunakan OpenGL pada python yang disediakan oleh library PyOpenGL, pertama kita melakukan import terlebih dahulu library yang akan digunakan,

```python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
```
Disini kami melakukan inisialisasi titik pada sebuah kotak
* variable _nx_ dan _ny_ adalah variable untuk melakukan scaling pada window agar terlihat lebih besar

* _x1,y1, x2, y2_ adalah variable titik garis yang akan di clipping

```python
# Insialisasi titik x_min, y_min, sebelum
x_min, y_min = 50, 50 
x_max, y_max = 100, 100

#Inisialisasi koordinat tempat scaling kotak,
nx_min, ny_min = 200, 200
nx_max, ny_max = 350, 350

#Inisialisasi t1 dan t2
t1, t2 = 0.0, 1.0

#inisialisasi titik garis
x1, y1 = 0, 0
x2, y2 = 100, 150
```

## Method atau Function untuk cetak pixel pada window
Disini kami membuat function atau method untuk memprojeksikan titik pada window

```python
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
    
    #Penggambaran pixel kotak, menggunakan GL_LINE_LOOP yang akan digunakan untuk menghubungi titik satu sama lain
    glColor3d(1, 0, 0)
    glBegin(GL_LINE_LOOP)
    glVertex2d(x_min, y_min) 
    glVertex2d(x_max, y_min)
    glVertex2d(x_max, y_max)
    glVertex2d(x_min, y_max)
    glEnd()
  
    #Penggambaran pixel garis, menggunakan GL_LINES yang akan digunakan untuk menghubungkan titik x1,y1 dan x2,y2 
    glColor3d(1, 1, 1)
    glBegin(GL_LINES)
    glVertex2d(x1, y1)
    glVertex2d(x2, y2)
    glEnd()
```

## Method atau Fungsi cliptest() yang digunakan untuk cek parameter
![Image of Parameter](https://i.ibb.co/qNpS4t9/nilai-p.png)
```python
def cliptest(p, q):
    t = q / p
    global t1, t2
    if p == 0 and q < 0:
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
```

## Method atau fungis liangbarsky()
```python
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
            "Titik Bawah Berpotong Pada Atas x = {} dan y = {}".format(
                nx1_real, ny1_real
            )
        )
        glVertex2d(nx2, ny2)
        print(
            "Titik Bawah Berpotong Pada Bawah x = {} dan y = {}".format(
                nx2_real, ny2_real
            )
        )
        glVertex2d(nx1_real, ny1_real)
        glVertex2d(nx2_real, ny2_real)
        glEnd()
```

## Method main()

```python
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
```


# Studi Kasus ...

Disini kami akan mencoba atau melakukan testing , antara lain sebagai berikut

1. Garis Melewati / Memotong semua kotak
2. Garis Hanya memotong sebagian dengan x1,y1 berada pada luar kotak dan x2,y2 berada dalam kotak
3. Garis Hanya memotong sebagaian dengan x1,y1 berada pada dalam kotak dan x2,y2 berada diluar kotak

> Garis Melewati / Memotong Semua Kotak

```python
x1, y1 = 0, 0
x2, y2 = 100, 150
```
![Image of Garis Memotong Semua](https://i.ibb.co/RQdCBcz/image.png)

Dengan titik potong berada pada

![Image of Titik Potong](https://i.ibb.co/kmnDYhc/image.png)
