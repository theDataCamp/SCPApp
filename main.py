import tkinter as tk
from tkinter import filedialog, messagebox
import paramiko
from scp import SCPClient
from paramiko import SSHClient
import threading


class SCPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SCP File Transfer")
        self.geometry("400x200")

        # GUI components setup
        tk.Label(self, text="Server:").grid(row=0, column=0, sticky="w")
        self.server_entry = tk.Entry(self)
        self.server_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(self, text="Port:").grid(row=1, column=0, sticky="w")
        self.port_entry = tk.Entry(self)
        self.port_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(self, text="Username:").grid(row=2, column=0, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(self, text="Password:").grid(row=3, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(self, text="File Path:").grid(row=4, column=0, sticky="w")
        self.file_path_entry = tk.Entry(self)
        self.file_path_entry.grid(row=4, column=1, sticky="ew")
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=4, column=2, sticky="ew")

        tk.Label(self, text="Remote Path:").grid(row=5, column=0, sticky="w")
        self.remote_path_entry = tk.Entry(self)
        self.remote_path_entry.grid(row=5, column=1, sticky="ew")

        self.send_button = tk.Button(self, text="Send", command=self.start_scp_thread)
        self.send_button.grid(row=6, column=0, columnspan=3, sticky="ew")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def start_scp_thread(self):
        # Change button text to indicate operation is in progress
        self.send_button.config(text="Sending...", state="disabled")
        # Start the SCP operation in a separate thread
        threading.Thread(target=self.scp_file).start()

    def scp_file(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()
        file_path = self.file_path_entry.get()
        remote_path = self.remote_path_entry.get()

        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, port=port, username=username, password=password)

            scp = SCPClient(ssh.get_transport())
            scp.put(file_path, remote_path)
            scp.close()
            ssh.close()

            messagebox.showinfo("Success", "File transferred successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Ensure the button text is reset on both success and failure
            self.send_button.config(text="Send", state="normal")


if __name__ == "__main__":
    app = SCPApp()
    app.mainloop()
