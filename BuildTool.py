import tkinter as tk
from tkinter import filedialog
import subprocess
import json
import os

class DockerGUI:
    def __init__(self, root):
        self.root = root
        root.title('wasm Build Tool with Docker')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Load config file
        self.config_file = 'config.json'
        self.config_data = self.load_config()

        # Image name input
        tk.Label(root, text="Image Name:").grid(row=0, column=0)
        self.image_name_var = tk.StringVar(value=self.config_data.get('image_name', ''))
        tk.Entry(root, textvariable=self.image_name_var).grid(row=0, column=1)

        # Build source code file selection
        tk.Label(root, text="Source Code File:").grid(row=2, column=0)
        self.file_path_var = tk.StringVar(value=self.config_data.get('file_path', ''))
        tk.Entry(root, textvariable=self.file_path_var).grid(row=2, column=1)

        # File selection button
        tk.Label(root, text="Destination Directory:").grid(row=3, column=0)
        self.destination_var = tk.StringVar(value=self.config_data.get('destination', ''))
        tk.Entry(root, textvariable=self.destination_var).grid(row=3, column=1)
        
        # Docker build button
        tk.Button(root, text="Build Docker Image", command=self.build_docker).grid(row=4, column=1)

        # Docker run button
        tk.Button(root, text="Run Docker Image", command=self.run_docker).grid(row=5, column=1)

    def build_docker(self):
        image_name = self.image_name_var.get()

        # Docker build command
        command = f'docker build -t {image_name} .'
        subprocess.run(command, shell=True, check=True)

        tk.messagebox.showinfo("Success", "Docker Image Built Successfully")

    def run_docker(self):
        image_name = self.image_name_var.get()
        # Splitting path and name
        path, name = os.path.split(self.file_path_var.get())

        # Removing .cpp extension
        name = os.path.splitext(name)[0]

        container_name = image_name + "-container"
        destination = self.destination_var.get()

        # Docker run command
        command = f"/bin/bash -c 'source /emsdk/emsdk_env.sh && cd /usr/app && emcc -I/usr/include/eigen3 -I/usr/app/include -lembind -o build/{name}.js {name}.cpp'"
        subprocess.run(['docker', 'run', '-d','--name', container_name, image_name, 'tail', '-f', '/dev/null'])
        subprocess.run(['docker', 'cp', path + '/.', f'{container_name}:/usr/app'])
        subprocess.run(["docker", "exec", container_name, "sh", "-c", command])
        subprocess.run(['docker', 'cp', f'{container_name}:/usr/app/build', destination])
        subprocess.run(['docker', 'stop', container_name])
        subprocess.run(['docker', 'rm', container_name])

        tk.messagebox.showinfo("Success", "Docker Image Ran Successfully")

    def on_closing(self):
        # 프로그램 종료 시 설정 저장
        self.config_data = {
            'image_name': self.image_name_var.get(),
            'file_path': self.file_path_var.get(),
            'destination': self.destination_var.get()
        }

        self.save_config()
        self.root.destroy()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f)

if __name__ == "__main__":
    root = tk.Tk()
    gui = DockerGUI(root)
    root.mainloop()
