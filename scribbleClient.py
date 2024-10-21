import socket
import threading
import tkinter as tk

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("DRAW"):
                draw_on_canvas(message)
            else:
                update_chat(message)
        except:
            client_socket.close()
            break

def draw_on_canvas(data):
    # Example of handling drawing messages sent by the server
    command, x, y = data.split()
    canvas.create_oval(int(x), int(y), int(x) + 5, int(y) + 5, fill='black')

def send_guess():
    guess = guess_entry.get()
    client_socket.send(guess.encode('utf-8'))
    guess_entry.delete(0, 'end')

def on_mouse_drag(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x + 5, y + 5, fill='black')
    client_socket.send(f"DRAW {x} {y}".encode('utf-8'))

def update_chat(message):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message + '\n')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

def setup_gui():
    global canvas, guess_entry, chat_display
    window = tk.Tk()
    window.title("Pictionary")

    canvas = tk.Canvas(window, width=400, height=400, bg='white')
    canvas.pack()
    canvas.bind("<B1-Motion>", on_mouse_drag)

    guess_entry = tk.Entry(window)
    guess_entry.pack()

    send_button = tk.Button(window, text="Send Guess", command=send_guess)
    send_button.pack()

    chat_display = tk.Text(window, width=50, height=10, state=tk.DISABLED)
    chat_display.pack()

    window.mainloop()

# Setup Client Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5555))

# Start a thread to listen for messages from the server
threading.Thread(target=receive_messages, args=(client_socket,)).start()

# Start the GUI
setup_gui()