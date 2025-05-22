from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

def insert_canvas_toolbar(canvas, parent, x_canvas=680, y_canvas=240, x_toolbar=1150, y_toolbar=10):
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x=x_canvas, y=y_canvas)

    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.place(x=x_toolbar, y=y_toolbar)
    toolbar.update()