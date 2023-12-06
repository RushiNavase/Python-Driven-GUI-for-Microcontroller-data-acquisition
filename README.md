# Python-Driven-GUI-for-Microcontroller-data-acquisition
This GUI is designed using Python for remote data acquisition from a microcontroller to monitor and plot real-time data.
Hardware Used:STM32F103C8T6 Development board,potentiometer/LM35,FTDI or USB to TTL module,Jumper wires 
Software Used:VS code , python app(3.11,3.10,3.9),Keil u Vision
//Code Workflow in Python for GUI://

connect_menu_init()
   - Purpose: Initializes the main GUI window for the serial communication application.
   - Components:
     - Labels for port information.
     - Buttons for refreshing available COM ports and connecting/disconnecting.
     - A frame for displaying voltage information.
     - A real-time data plot using Matplotlib.

connect_check(args)
   - Purpose: Checks the selected COM port and baud rate to enable or disable the "Connect" button accordingly.
   - Components:
     - Disables the "Connect" button if an invalid COM port or baud rate is selected.
     - Enables the button otherwise.

baud_select()
   - Purpose: Creates a drop-down menu for selecting the baud rate.
   - Components:
     - Initializes a Tkinter `OptionMenu` with available baud rates.
     - Links the menu to the `connect_check` function to update the "Connect" button status.

update_coms()
   - Purpose: Dynamically updates the available COM ports in the drop-down menu.
   - Components:
     - Uses the `serial.tools.list_ports` module to detect connected COM ports.
     - Updates the COM port drop-down menu.

plot_data(i, ax)
   - Purpose: Plots the real-time ADC data on the Matplotlib chart.
   - Components:
     - Clears the previous plot.
     - Plots the latest data points.
     - Sets axis labels and grid.

ReadSerial()
   - Purpose: Reads and processes data from the serial port continuously.
   - Components:
     - Maintains a buffer for incoming serial data.
     - Decodes and processes the data.
     - Updates the voltage label and appends data for plotting.

connection()
   - Purpose: Manages the Connect/Disconnect button behavior and establishes/terminates the serial connection.
   - Components:
     - Toggles between "Connect" and "Disconnect" states.
     - Disables/enables relevant buttons and drop-down menus.
     - Establishes or terminates the serial connection.

close_window()
   - Purpose: Ensures proper termination of the program when the user closes the GUI window.
   - Components:
     - Stops the continuous data reading thread.
     - Destroys the Tkinter root window.

Main Loop
   - Purpose: Initiates the main event loop for the Tkinter application, keeping the GUI responsive.

Termination
    - Purpose: Allows the program to be closed gracefully by clicking the window close button or using the "Disconnect" button.


//Code workflow for Microcontroller code://

