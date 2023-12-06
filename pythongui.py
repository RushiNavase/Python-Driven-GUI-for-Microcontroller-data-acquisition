from tkinter import *
import serial.tools.list_ports
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import time

# Global variables for storing data
x_data = []
y_data = []
serialData = False
ser = None



def connect_menu_init():
    global root, connect_btn, refresh_btn, voltage_frame, voltage_label, x_data, y_data, ani
    root = Tk()
    root.title("Serial Communication")
    root.geometry("1200x600")
    root.resizable(width=False, height=False)

    root.config(bg="white")

    port_label = Label(root, text="Available Port(s):", bg="white")
    port_label.grid(column=1, row=2, padx=10, pady=20)

    port_bd = Label(root, text="Baud rate:", bg="white")
    port_bd.grid(column=1, row=3, padx=10, pady=20)

    refresh_btn = Button(root, text="R", height=2, width=10, command=update_coms)
    refresh_btn.grid(column=3, row=2)

    connect_btn = Button(root, text="Connect", height=2, width=10, state="disabled", command=connection)
    connect_btn.grid(column=3, row=4)

    voltage_frame = Frame(root, relief="groove", borderwidth=4)
    voltage_frame.grid(column=1, row=6, pady=20, padx=5)

    voltage_label = Label(voltage_frame, text="Volatge: ", bg="white", font=("Helvetica", 12))
    voltage_label.pack()

    fig, ax = plt.subplots()
    ax.set_title('Real-Time ADC Data Plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('ADC data')
    ax.grid(True)

    chart = FigureCanvasTkAgg(fig, master=root)
    chart.get_tk_widget().grid(column=6, row=1, columnspan=6, rowspan=6)

    x_data = []
    y_data = []

    baud_select()
    update_coms()

    ani = FuncAnimation(fig, plot_data, fargs=(ax,), interval=500)

def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"

def baud_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "56000", "57600",
            "115200", "128000", "256000"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(root, clicked_bd, *bds, command=connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)

def update_coms():
    global clicked_com, drop_COM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        drop_COM.destroy()
    except:
        pass

    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_COM = OptionMenu(root, clicked_com, *coms, command=connect_check)
    drop_COM.config(width=20)
    drop_COM.grid(column=2, row=2, padx=50)
    connect_check(0)

def plot_data(i, ax):
    ax.clear()
    ax.plot(x_data, y_data, label='ADC Data')
    ax.set_ylim(0, 5)
    ax.legend()
    ax.grid(True)

def ReadSerial():
    global serialData, voltage_label, x_data, y_data

    buffer = b''

    while serialData:
        data = ser.read()
        if len(data) > 0:
            try:
                decoded_data = data.decode('utf-8')

                if decoded_data.isdigit() or decoded_data == '.':
                    buffer += data
                elif decoded_data == '\n':
                    cleaned_buffer = buffer.replace(b'\r', b'').replace(b'\n', b'')
                    sensor_value = float(cleaned_buffer)

                    voltage_label.config(text=f"Voltage: {sensor_value:.3f} V")

                    x_data.append(time.time())
                    y_data.append(sensor_value)

                    N = 50
                    x_data = x_data[-N:]
                    y_data = y_data[-N:]

                    buffer = b''

            except (UnicodeDecodeError, ValueError) as e:
                print(f"Error: {e}")
                buffer = b''

def connection():
    global ser, serialData
    if connect_btn["text"] in "Disconnect":
        serialData = False
        connect_btn["text"] = "connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"

    else:
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disable"
        drop_bd["state"] = "disable"
        drop_COM["state"] = "disable"
        port = clicked_com.get()
        baud = clicked_bd.get()

        try:
            ser = serial.Serial(port, baud, timeout=0)
        except:
            pass
        t1 = threading.Thread(target=ReadSerial)
        t1.daemon = True
        t1.start()

def close_window():
    global root, serialData
    serialData = False
    root.destroy()

connect_menu_init()
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()
