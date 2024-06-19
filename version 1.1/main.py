import os.path
import subprocess
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import minecraft_launcher_lib as mclib
import minecraftVersions


class MinecraftLauncher:
    def __init__(self):
        self.run_ver = 0
        if not os.path.exists(".minecraft"):
            os.mkdir(".minecraft")
            self.minecraft_dir_path = ".minecraft"
        else:
            self.minecraft_dir_path = ".minecraft"
        self.PMCL = tk.Tk()
        self.PMCL.title("Python Minecraft Launcher")
        self.PMCL.geometry("1200x800")
        self.selected_version = ""
        self.current_max = 0
        self.callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max
        }

        self.PMCL_Main_Menu = tk.Menu(self.PMCL)
        self.PMCL.config(menu=self.PMCL_Main_Menu)
        # 菜单-文件
        self.PMCL_File = tk.Menu(self.PMCL_Main_Menu, tearoff=0)
        self.PMCL_Main_Menu.add_cascade(label="文件", menu=self.PMCL_File)
        self.PMCL_File.add_command(label="从外部导入minecraft文件夹")
        # 菜单-PMCL设置
        self.PMCL_Settings = tk.Menu(self.PMCL_Main_Menu, tearoff=0)
        self.PMCL_Main_Menu.add_cascade(label="PMCL设置", menu=self.PMCL_Settings)

        self.PMCL_Notepad_bar = ttk.Notebook(self.PMCL)
        self.PMCL_Menu = ttk.Frame()
        self.PMCL_Download = ttk.Frame()
        self.PCML_Download_Log = ttk.Frame()
        self.sby = ttk.Scrollbar(self.PCML_Download_Log, orient=tk.VERTICAL)
        self.PCML_Download_Log_Text = tk.Text(self.PCML_Download_Log, yscrollcommand=self.sby.set, width=100000,
                                              height=100000)
        self.sby.pack(side="right", fill="y")
        self.sby.config(command=self.PCML_Download_Log_Text.yview)
        self.PCML_Download_Log_Text.pack()
        self.PMCL_Notepad_bar.add(self.PMCL_Menu, text="首页")
        self.PMCL_Notepad_bar.add(self.PMCL_Download, text="下载Minecraft版本")
        self.PMCL_Notepad_bar.add(self.PCML_Download_Log, text="下载日志")
        self.PMCL_Notepad_bar.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.version_list = tk.Listbox(self.PMCL_Download, background="skyblue", width=40)
        self.version_list.pack(fill="y", side="left")
        self.mclist = minecraftVersions.MCVersion().getAllVersions().toList()
        for i in self.mclist:
            self.version_list.insert(tk.END, i)
        self.version_list.bind("<<ListboxSelect>>", self.get_download_version)
        ttk.Button(self.PMCL_Download, command=self.download_threading_start, text="下载选中版本").pack(side="left")

        t2 = ttk.Scrollbar(self.PMCL_Menu, orient=tk.VERTICAL)
        self.minecraft_version_list = os.listdir(".minecraft/versions")
        self.vl = tk.Listbox(self.PMCL_Menu, background="skyblue", yscrollcommand=t2.set, width=40)
        t2.pack(side=tk.RIGHT, fill=tk.Y)
        t2.config(command=self.vl.yview)
        self.vl.pack(fill="y", side="right")
        for i in self.minecraft_version_list:
            self.vl.insert(tk.END, i)
        ttk.Label(self.PMCL_Menu, text="欢迎来到Python Minecraft Launcher v1.1!", font=("宋体", 20)).pack(pady=50)
        photo = tk.PhotoImage(file="steve.png")
        self.steve = ttk.Label(self.PMCL_Menu, image=photo)
        self.steve.pack(pady=100)
        style = ttk.Style()

        style.configure('RoundedButton.TButton',
                        foreground='black',
                        borderwidth=0,
                        relief=tk.RAISED)
        self.l1 = ttk.Label(self.PMCL_Menu, text="输入用户名:\t")
        self.l1.pack(side="left")
        self.username = ttk.Entry(self.PMCL_Menu)
        self.username.pack(side="left")
        self.start = ttk.Button(self.PMCL_Menu, text="启动选中的游戏", style='RoundedButton.TButton',
                                command=self.threading_starting)
        self.start.pack(side="right")
        self.PMCL.mainloop()

    def threading_starting(self):
        s1 = threading.Thread(target=self.get_version_to_start)
        s1.start()

    def set_status(self, status: str):
        self.PCML_Download_Log_Text.insert(tk.END, f"\n{status}")

    def set_progress(self, progress: int):
        if self.current_max != 0:
            self.PCML_Download_Log_Text.insert(tk.END, f"\n{progress}/{self.current_max}")

    def set_max(self, new_max: int):
        self.current_max = new_max

    def get_download_version(self, *args):
        self.selected_version = self.mclist[
            self.version_list.curselection()[0] if len(self.version_list.curselection()) != 0 else 0]

    def download_minecraft_version(self):
        ui = tk.Tk()

        def fheuifhuegfuewgfu():
            if self.selected_version != "":
                ui.title("下载版本-" + self.selected_version)
                ui.geometry("500x400")
                vs = self.selected_version
                tk.Label(ui, text="下载 " + self.selected_version).pack()

                def choose(*args):
                    if a.get() == "Minecraft Forge":
                        ui.title("下载版本-" + vs + " - Forge")
                        ui.update()
                    else:
                        ui.title("下载版本-" + vs + " - Fabric")
                        ui.update()

                if mclib.fabric.is_minecraft_version_supported(vs) and mclib.forge.find_forge_version(vs) is not None:
                    tk.Label(ui, text="选择要下载的Minecraft mod加载器").pack()
                    a = ttk.Combobox(ui, state="readonly")
                    a.pack()
                    a["value"] = ("Minecraft Forge", "Minecraft Fabric")
                    a.bind("<<ComboboxSelected>>", choose)

                def download_choose():
                    try:
                        if a.get() == "Minecraft Forge":
                            ui.destroy()
                            mclib.install.install_minecraft_version(vs, self.minecraft_dir_path, callback=self.callback)
                            mclib.forge.install_forge_version(mclib.forge.list_forge_versions()[0],
                                                              self.minecraft_dir_path,
                                                              callback=self.callback)
                            msgbox.showinfo("Python Minecraft Launcher", "下载成功!")
                            self.minecraft_version_list = os.listdir(".minecraft/versions")
                            self.vl.delete(0, "end")
                            for i in self.minecraft_version_list:
                                self.vl.insert(tk.END, i)
                        elif a.get() == "Minecraft Fabric":
                            if mclib.fabric.is_minecraft_version_supported(vs):
                                ui.destroy()
                                try:
                                    mclib.install.install_minecraft_version(vs, self.minecraft_dir_path,
                                                                            callback=self.callback)
                                    mclib.fabric.install_fabric(vs, self.minecraft_dir_path, callback=self.callback)
                                    msgbox.showinfo("Python Minecraft Launcher", "下载成功!")
                                    self.minecraft_version_list = os.listdir(".minecraft/versions")
                                    self.vl.delete(0, "end")
                                    for i in self.minecraft_version_list:
                                        self.vl.insert(tk.END, i)
                                except Exception as exp:
                                    msgbox.showerror("Python Minecraft Launcher", f"下载失败:{exp}")
                    except NameError:
                        ui.destroy()
                        mclib.install.install_minecraft_version(vs, self.minecraft_dir_path, callback=self.callback)
                        msgbox.showinfo("Python Minecraft Launcher", "下载成功!")
                        self.minecraft_version_list = os.listdir(".minecraft/versions")
                        self.vl.delete(0, "end")
                        for i in self.minecraft_version_list:
                            self.vl.insert(tk.END, i)

                b = tk.Button(ui, text="下载所选版本-Minecraft " + self.selected_version, command=download_choose)
                b.pack()
            else:
                msgbox.showerror("Python Minecraft Launcher", "喵的！你还没有选中版本下个屁的下！")
                ui.destroy()

        fheuifhuegfuewgfu()
        ui.mainloop()

    def get_version_to_start(self, *args):
        self.run_ver = self.minecraft_version_list[self.vl.curselection()[0]]
        callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max
        }
        options = {
            "username": self.username.get(),
            "-Dminecraft.launcher.brand": "PMCL Launcher",
            "-Dminecraft.launcher.version": "1.1.1",
            "--accessToken": "",
            "--userType": "Legacy"
        }
        minecraft_command = mclib.command.get_minecraft_command(
            self.run_ver, self.minecraft_dir_path, options)
        try:
            subprocess.call(minecraft_command)
            # raise RuntimeError
        except:
            import json
            a = open(f".minecraft/versions/{self.run_ver}/{self.run_ver}.json", "w")
            b = "".join(a.read().split('"--uuid", "${auth_uuid}", '))
            a.write(b)
            subprocess.call(minecraft_command)

    def download_threading_start(self):
        s2 = threading.Thread(target=self.download_minecraft_version)
        s2.start()


MinecraftLauncher()
