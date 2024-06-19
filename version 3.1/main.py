import os.path
import subprocess
import threading
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import minecraft_launcher_lib as mclib
import tkinter.filedialog as fdl
import ttkthemes
import py_mc_lib


class MinecraftLauncher:
    def init_win(self):
        self.mclist = []
        root = tk.Tk()
        root.title("居中的窗口")
        root.overrideredirect(True)
        screenWidth = root.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = root.winfo_screenheight()  # 获取显示区域的高度
        root.wm_attributes("-topmost", 1)
        width = 128  # 设定窗口宽度
        height = 128  # 设定窗口高度
        left = (screenWidth - width) // 2
        top = (screenHeight - height) // 2

        def load_mclist():
            self.mclist = py_mc_lib.JavaClient.VersionManifest().get_versions()

        image_dh = tk.PhotoImage(file="./PML/PixelarticonsPixelarticons.png")
        tk.Label(root, image=image_dh).pack()
        # 宽度x高度+x偏移+y偏移
        # 在设定宽度和高度的基础上指定窗口相对于屏幕左上角的偏移位置
        root.geometry("%dx%d+%d+%d" % (width, height, left, top))
        s6 = threading.Thread(target=load_mclist)
        s6.start()
        while True:
            if self.mclist:
                root.destroy()
                break
            else:
                root.update()

    def __init__(self):
        self.init_win()
        self.run_ver = 0
        tmp_path = open("PML/folder_last_open.txt")
        path_tmp = tmp_path.read()
        if os.path.isdir(os.path.abspath(path_tmp)):
            self.minecraft_dir_path = path_tmp
        else:
            self.minecraft_dir_path = ".minecraft"
        tmp_path.close()
        self.PML = tk.Tk()
        self.PML.title("Pixel Minecraft Launcher")
        self.PML.geometry("1300x800")
        self.PML.iconbitmap("PML/ddd.ico")
        tmp_dgu = open("PML/file_last_open.flo").read()
        if tmp_dgu != "" or not tmp_dgu.isspace():
            try:
                tmp_gdu1 = open(tmp_dgu).read()
                self.loadthemepack(tmp_gdu1)
            except:
                pass
        self.selected_version = ""
        self.current_max = 0
        namelist = open("PML/namelist.nl")
        self.namelist = namelist.read().split("\n")
        namelist.close()
        self.callback = {
            "setStatus": self.set_status,
            "setProgress": self.set_progress,
            "setMax": self.set_max
        }
        with open("PML/version_last_open.vlo") as r:
            self.selected_version_to_start = r.read()
        self.minecraft_version_list = os.listdir(self.minecraft_dir_path + r"\versions")

        self.PML_Notepad_bar = ttk.Notebook(self.PML)
        self.PML_Menu = ttk.Frame()
        self.PML_Download = ttk.Frame()
        self.PML_Settings = ttk.Frame()
        self.PML_Notepad_bar.add(self.PML_Menu, text="首页")
        self.PML_Notepad_bar.add(self.PML_Download, text="下载Minecraft版本")
        self.PML_Notepad_bar.add(self.PML_Settings, text="设置")
        self.PML_Notepad_bar.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.textvar = tk.StringVar()
        self.textvar.set("下载状态：")
        self.label = tk.Label(self.PML, textvariable=self.textvar, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

        self.version_list = tk.Listbox(self.PML_Download, background="skyblue", width=40)
        self.version_list.pack(fill="y", side="left")
        for i in self.mclist:
            self.version_list.insert(tk.END, i)
        self.version_list.bind("<<ListboxSelect>>", self.get_download_version)
        ttk.Button(self.PML_Download, command=self.download_threading_start, text="下载选中版本").pack(side="left",
                                                                                                       anchor="n")
        ttk.Label(self.PML_Download, text="或者输入版本→").pack(side="left", anchor="n")
        self.Find_version = tk.Entry(self.PML_Download)
        self.Find_version.pack(side="left", anchor="n", pady=5)
        self.Current_version = ttk.Button(self.PML_Download, text="下载输入的版本",
                                          command=self.download_sddsidga_start)
        self.Current_version.pack(side="left", anchor="n", pady=5)

        self.Set_PML_Theme = tk.Button(self.PML_Settings, text="导入PML配置文件", command=self.importthemepack)
        self.Set_PML_Theme.pack(side="left", anchor="n")
        self.advanced_settings_var = tk.IntVar()
        self.advanced_settings = tk.Checkbutton(self.PML_Settings, text="打开实验性功能", command=self.enable_PSL,
                                                variable=self.advanced_settings_var)
        self.advanced_settings.pack(side="left", anchor="n")

        photo = tk.PhotoImage(file="PML/PixelarticonsPixelarticons.png")
        self.steve = ttk.Label(self.PML_Menu, image=photo)
        self.steve.pack(pady=50)
        ttk.Label(self.PML_Menu, text="欢迎来到Pixel Minecraft Launcher v3.1!", font=("宋体", 20)).pack(pady=50)
        style = ttk.Style()
        style.configure('RoundedButton.TButton',
                        foreground='black',
                        borderwidth=0,
                        relief=tk.RAISED)
        self.l1 = ttk.Label(self.PML_Menu, text="↓---输入用户名---↓")
        self.l1.pack()
        self.username = ttk.Combobox(self.PML_Menu, width=22, values=self.namelist)
        self.username.pack()
        self.version_start_var = tk.StringVar()
        self.version_start_var.set(f"启动选中的游戏\n{self.selected_version_to_start}")
        self.start = tk.Button(self.PML_Menu, textvariable=self.version_start_var, command=self.threading_starting,
                               width=30, anchor="center", borderwidth=1, relief="flat")
        self.changever = tk.Button(self.PML_Menu, text="版本选择", command=self.select_version_0,
                                   width=30, anchor="center", borderwidth=1, relief="flat")
        self.start.pack()
        tk.Label().pack()
        self.changever.pack()
        self.PML.mainloop()
        with open("PML/folder_last_open.txt", "w") as flo:
            flo.write(self.minecraft_dir_path)

    def enable_PSL(self):
        if self.advanced_settings_var.get() == 1:
            self.butt = tk.Button(self.PML_Settings, text="打开Pixel Server Launcher(实验性)")
            self.butt.pack(side="left", anchor="n")
        else:
            self.butt.destroy()

    def change(self):
        if self.username.get().isspace() or self.username.get() in self.namelist:
            pass
        else:
            self.namelist.append(self.username.get())
            self.username["value"] = self.namelist
            with open("PML/namelist.nl", "a") as f:
                f.write(self.username.get() + "\n")

    def find_and_download_version(self):
        if self.Find_version.get() in self.mclist:
            ui = tk.Tk()
            self.selected_version = self.Find_version.get()

            def fheuifhuegfuewgfu():
                ui.title("下载版本-" + self.selected_version)
                ui.geometry("500x400")
                ui.iconbitmap("PML/ddd.ico")
                vs = self.selected_version
                tk.Label(ui, text="下载 " + self.selected_version).pack()

                def choose(*args):
                    if a.get() == "Minecraft Forge":
                        ui.title("下载版本-" + vs + " - Forge")
                        ui.update()
                    else:
                        ui.title("下载版本-" + vs + " - Fabric")
                        ui.update()

                if mclib.fabric.is_minecraft_version_supported(vs) and mclib.forge.find_forge_version(
                        vs) is not None:
                    tk.Label(ui, text="选择要下载的Minecraft mod加载器").pack()
                    a = ttk.Combobox(ui, state="readonly")
                    a.pack()
                    a["value"] = ("Minecraft Forge", "Minecraft Fabric")
                    a.bind("<<ComboboxSelected>>", choose)

                def download_choose():
                    try:
                        if a.get() == "Minecraft Forge":
                            ui.destroy()
                            mclib.install.install_minecraft_version(vs, self.minecraft_dir_path,
                                                                    callback=self.callback)
                            mclib.forge.install_forge_version(mclib.forge.list_forge_versions()[0],
                                                              self.minecraft_dir_path,
                                                              callback=self.callback)
                            msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                            self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
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
                                    msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                                except Exception as exp:
                                    msgbox.showerror("Pixel Minecraft Launcher", f"下载失败:{exp}")
                    except NameError:
                        ui.destroy()
                        try:
                            mclib.install.install_minecraft_version(vs, self.minecraft_dir_path,
                                                                    callback=self.callback)
                        except Exception as exp:
                            msgbox.showerror("Pixel Minecraft Launcher", f"下载失败:{exp}")
                        msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                        self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
                        self.vl.delete(0, "end")
                        for i in self.minecraft_version_list:
                            self.vl.insert(tk.END, i)

                b = tk.Button(ui, text="下载所选版本-Minecraft " + self.selected_version, command=download_choose)
                b.pack()

            fheuifhuegfuewgfu()
            ui.mainloop()

    def loadthemepack(self, themepack):
        tmp_dhhhh = themepack.split("\n")
        for i in tmp_dhhhh:
            match i.lower():
                case _ if i.lower().startswith("theme:"):
                    if i[5:-1] == "" or i[5:-1].isspace():
                        self.PML_style = ttkthemes.ThemedStyle(self.PML)
                        self.PML_style.set_theme(i[5:-1])
                    else:
                        self.PML_style = ttkthemes.ThemedStyle(self.PML)
                        self.PML_style.set_theme("adapta")

                case _ if i.lower().startswith("title:"):
                    if not (i[6:] == "") or not (i[6:].isspace()):
                        self.PML.title(i[6:])

                case _:
                    self.PML_style = ttkthemes.ThemedStyle(self.PML)
                    self.PML_style.set_theme("adapta")

    def importthemepack(self):
        filepath = fdl.askopenfilename(filetype=[("themepack文件", "*.PMLthemepack")])
        if filepath == "" or filepath.isspace():
            pass
        else:
            self.loadthemepack(open(os.path.abspath(filepath)).read())

    def change_version(self, *args):
        self.selected_version_to_start = self.vl.get(self.vl.curselection()[0])
        self.version_start_var.set(f"启动选中的游戏\n{self.selected_version_to_start}")
        with open("PML/version_last_open.vlo", "w") as f:
            f.write(self.selected_version_to_start)

    def close_win(self, *args):
        self.win.destroy()

    def select_version_0(self):
        self.win = tk.Tk()
        self.win.title("PML|版本选择")
        self.win.geometry("500x600")
        self.win.iconbitmap("PML/ddd.ico")

        tk.Button(self.win, text="更换minecraft文件夹", command=self.open_other_minecraft_folder).pack(side="left",
                                                                                                       anchor="n")

        t2 = ttk.Scrollbar(self.win, orient=tk.VERTICAL)
        self.vl = tk.Listbox(self.win, background="skyblue", yscrollcommand=t2.set, width=40)
        t2.pack(side=tk.RIGHT, fill=tk.Y)
        self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
        self.vl.delete(0, "end")
        for i in self.minecraft_version_list:
            self.vl.insert(tk.END, i)
        t2.config(command=self.vl.yview)
        self.vl.pack(fill="y", side="right")
        self.vl.bind("<<ListboxSelect>>", self.change_version)
        self.vl.bind("<Double-Button-1>", self.close_win)

        self.win.mainloop()

    def threading_starting(self):
        s1 = threading.Thread(target=self.get_version_to_start)
        s1.start()

    def open_other_minecraft_folder(self):
        tmp = fdl.askdirectory(title="打开Minecraft文件夹")
        if tmp != "":
            try:
                self.minecraft_dir_path = tmp
                self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
                self.vl.delete(0, "end")
                for i in self.minecraft_version_list:
                    self.vl.insert(tk.END, i)
            except:
                msgbox.showerror("Pixel Minecraft Launcher",
                                 "无法读取指定目录下的version文件夹\n您所选择的文件夹是否正确?")

    def set_status(self, status: str):
        self.textvar.set(f"下载状态：{status}")
        self.label.update()

    def set_progress(self, progress: int):
        if self.current_max != 0:
            self.textvar.set(f"下载状态:{progress}/{self.current_max}")

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
                ui.iconbitmap("PML/ddd.ico")
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
                            msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                            self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
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
                                    msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                                except Exception as exp:
                                    msgbox.showerror("Pixel Minecraft Launcher", f"下载失败:{exp}")
                    except NameError:
                        ui.destroy()
                        try:
                            mclib.install.install_minecraft_version(vs, self.minecraft_dir_path, callback=self.callback)
                        except Exception as exp:
                            msgbox.showerror("Pixel Minecraft Launcher", f"下载失败:{exp}")
                        msgbox.showinfo("Pixel Minecraft Launcher", "下载成功!")
                        self.minecraft_version_list = os.listdir(f"{self.minecraft_dir_path}/versions")
                        try:
                            self.vl.delete(0, "end")
                            for i in self.minecraft_version_list:
                                self.vl.insert(tk.END, i)
                        except:
                            pass

                b = tk.Button(ui, text="下载所选版本-Minecraft " + self.selected_version, command=download_choose)
                b.pack()
            else:
                msgbox.showerror("Pixel Minecraft Launcher", "喵的！你还没有选中版本下个屁的下！")
                ui.destroy()

        fheuifhuegfuewgfu()
        ui.mainloop()

    def get_version_to_start(self, *args):
        if self.username.get() == "" or self.username.get().isspace():
            msgbox.showerror("Pixel Minecraft Launcher", "你还没有填写用户名!")
        else:
            if self.selected_version_to_start in self.minecraft_version_list:
                self.run_ver = self.selected_version_to_start
                callback = {
                    "setStatus": self.set_status,
                    "setProgress": self.set_progress,
                    "setMax": self.set_max
                }
                options = {
                    "username": self.username.get(),
                    "-Dminecraft.launcher.brand": "PML Launcher",
                    "-Dminecraft.launcher.version": "3.1",
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
                    a = open(f"{self.minecraft_dir_path}/versions/{self.run_ver}/{self.run_ver}.json", "w")
                    b = "".join(a.read().split('"--uuid", "${auth_uuid}", '))
                    a.write(b)
                    subprocess.call(minecraft_command)
            else:
                msgbox.showerror("Pixel Minecraft Launcher", "版本不可用!")

    def download_threading_start(self):
        s2 = threading.Thread(target=self.download_minecraft_version)
        s2.start()

    def download_sddsidga_start(self):
        s4 = threading.Thread(target=self.find_and_download_version)
        s4.start()


try:
    MinecraftLauncher()
except threading.ThreadError:
    pass
