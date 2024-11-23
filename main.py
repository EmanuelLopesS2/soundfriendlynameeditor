import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import ctypes
import sys
import base64

def set_dark_theme():
    # Cores
    DARK_BG = '#2b2b2b'        # Cinza escuro para o fundo
    DARKER_BG = '#232323'      # Cinza mais escuro para elementos
    LIGHTER_BG = '#333333'     # Cinza mais claro para elementos interativos
    ENTRY_BG = '#3c3c3c'       # Cinza ainda mais claro para entrada de texto
    BUTTON_BG = '#404040'      # Cinza para botões
    BUTTON_HOVER = '#4a4a4a'   # Cinza mais claro para hover dos botões
    TEXT_COLOR = '#ffffff'     # Texto branco
    SELECTED_BG = '#505050'    # Cor de seleção
    
    # Configuração do tema
    style = ttk.Style()
    
    # Frame
    style.configure('TFrame', background=DARK_BG)
    
    # Treeview
    style.configure('Treeview',
        background=DARKER_BG,
        foreground=TEXT_COLOR,
        fieldbackground=DARKER_BG,
        borderwidth=0
    )
    style.configure('Treeview.Heading',
        background='#006400',        # Verde escuro (DarkGreen)
        foreground=TEXT_COLOR,
        borderwidth=0,
        relief='flat'
    )
    style.map('Treeview.Heading',
        background=[('active', '#006400')],  # Mesmo verde no hover
        relief=[('active', 'flat')]
    )
    style.map('Treeview',
        background=[('selected', SELECTED_BG)],
        foreground=[('selected', TEXT_COLOR)]
    )
    
    # Entry
    style.configure('Dark.TEntry',
        fieldbackground=ENTRY_BG,
        foreground=TEXT_COLOR,
        insertcolor=TEXT_COLOR,
        borderwidth=0
    )
    style.map('Dark.TEntry',
        fieldbackground=[('focus', ENTRY_BG)],
        bordercolor=[('focus', ENTRY_BG)]
    )
    
    # Label
    style.configure('TLabel',
        background=DARK_BG,
        foreground=TEXT_COLOR
    )
    
    return style

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def create_device_frame(root):
    # Adicionar esta função no início de create_device_frame
    def load_devices():
        # Limpa a treeview
        for item in tree.get_children():
            tree.delete(item)
            
        ps_command = '''
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $OutputEncoding = [System.Text.Encoding]::UTF8
        [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        
        Write-Host "`nListing Audio Devices:" -ForegroundColor Green
        Write-Host "--------------------" -ForegroundColor Green
        
        $devices = Get-PnpDevice -Class "MEDIA" -Status OK | ForEach-Object {
            $name = [System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes($_.FriendlyName))
            $id = $_.InstanceId
            
            Write-Host "$name" -ForegroundColor Yellow
            Write-Host "ID: $id`n" -ForegroundColor Gray
            
            # Retorna para o pipe
            "$name|$id"
        }
        
        # Retorna os dados para o Python
        $devices
        '''
        
        try:
            # Primeiro executa o comando para mostrar no terminal
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                check=True
            )
            
            # Depois executa para capturar os dados
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            tree.device_data = {}
            index = 1  # Inicializa o contador em 1
            
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    name, device_id = line.strip().split('|')
                    name = name.strip()
                    device_id = device_id.strip()
                    
                    item_id = tree.insert('', 'end', values=(str(index), name), tags=('item',))
                    tree.device_data[item_id] = {'id': device_id, 'original_name': name}
                    index += 1  # Incrementa o contador
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load devices: {str(e)}")
    
    # Main frame
    frame = ttk.Frame(root, padding="5", style='TFrame')
    frame.grid(row=0, column=0, sticky="nsew")
    
    # Background frame
    background_frame = tk.Frame(frame, bg='#232323')
    background_frame.grid(row=0, column=0, sticky="nsew")
    
    # Configure treeview style
    style = ttk.Style()
    style.layout("Custom.Treeview", [
        ('Custom.Treeview.treearea', {'sticky': 'nswe'})
    ])
    
    # Configure colors and fonts
    style.configure("Custom.Treeview",
        background='#232323',
        foreground='white',
        fieldbackground='#232323',
        borderwidth=0,
        font=('Segoe UI', 10),
        rowheight=25
    )
    
    # Create treeview without headers
    tree = ttk.Treeview(
        background_frame,
        columns=("index", "name"), 
        show="",  # Remove headers
        height=10,
        style="Custom.Treeview",
        selectmode="browse"
    )
    
    # Configure mouse wheel scroll
    def on_mousewheel(event):
        tree.yview_scroll(int(-1*(event.delta/120)), "units")
    
    tree.bind('<MouseWheel>', on_mousewheel)
    
    # Configure item colors
    tree.tag_configure('item', background='#232323')
    
    tree.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    
    # Configure columns
    tree.column("index", width=30, anchor="center", minwidth=30)
    tree.column("name", width=481, minwidth=200)
    
    # Configure grid
    background_frame.columnconfigure(0, weight=1)
    background_frame.rowconfigure(0, weight=1)
    
    # Edit frame
    edit_frame = ttk.Frame(frame, style='TFrame')
    edit_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    
    # Name entry (sem a label)
    name_entry = tk.Entry(
        edit_frame,
        width=61,              # Aumentado de 54 para 61
        font=('Segoe UI', 10),
        bg='#3c3c3c',
        fg='white',
        insertbackground='white',
        relief='flat',
        highlightthickness=1,
        highlightbackground='#232323',
        highlightcolor='#505050'
    )
    name_entry.grid(row=0, column=0, padx=(0, 5))
    
    def on_select(event=None):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            name = item['values'][1]
            name_entry.delete(0, tk.END)
            name_entry.insert(0, name)
    
    def on_edit():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a device first.")
            return
        
        item_id = selected_items[0]
        if not hasattr(tree, 'device_data') or item_id not in tree.device_data:
            return
            
        device_data = tree.device_data[item_id]
        old_name = device_data['original_name']
        new_name = name_entry.get().strip()
        index_str = tree.item(item_id)['values'][0]
        
        if not new_name:
            messagebox.showwarning("Warning", "Please enter a new name.")
            return
            
        if new_name == old_name:
            return
            
        # Adiciona confirmação antes de fazer a mudança
        if not messagebox.askyesno("Confirm", 
            f"Do you want to change the device name?\n\n"
            f"From:\t{old_name}\n"
            f"To:\t{new_name}"):
            return
            
        # Aplica a mudança no registro do Windows
        ps_command = f'''
        $deviceID = "{device_data['id']}"
        $newName = '{new_name}'
        
        try {{
            $regPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$deviceID"
            Set-ItemProperty -Path $regPath -Name "FriendlyName" -Value $newName -ErrorAction Stop
            Write-Host "SUCCESS"
        }} catch {{
            Write-Host "ERROR: $($_.Exception.Message)"
        }}
        '''
        
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if "SUCCESS" in result.stdout:
                # Atualiza visualmente a treeview
                tree.item(item_id, values=(index_str, new_name))
                # Atualiza o nome original no device_data
                tree.device_data[item_id]['original_name'] = new_name
                
                # Atualiza a lista no PowerShell
                load_devices()
                
                if messagebox.askyesno(
                    "Success",
                    "Device name updated!\n\n"
                    "You need to restart Windows to apply the changes.\n\n"
                    "Do you want to restart now?"
                ):
                    subprocess.run(["shutdown", "/r", "/t", "0"])
            else:
                messagebox.showerror("Error", "Could not update device name. Make sure you have administrator privileges.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update device name: {str(e)}")
    
    def update_devices():
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        ps_command = '''
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        $OutputEncoding = [System.Text.Encoding]::UTF8
        [System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        
        Write-Host "`nListing Audio Devices:" -ForegroundColor Green
        Write-Host "--------------------" -ForegroundColor Green
        
        $devices = Get-PnpDevice -Class "MEDIA" -Status OK | ForEach-Object {
            $name = [System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes($_.FriendlyName))
            $id = $_.InstanceId
            
            Write-Host "$name" -ForegroundColor Yellow
            Write-Host "ID: $id`n" -ForegroundColor Gray
            
            # Retorna para o pipe
            "$name|$id"
        }
        
        # Retorna os dados para o Python
        $devices
        '''
        
        try:
            # Primeiro executa o comando para mostrar no terminal
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                check=True
            )
            
            # Depois executa para capturar os dados
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_command],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            tree.device_data = {}
            index = 1  # Inicializa o contador em 1
            
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    name, device_id = line.strip().split('|')
                    name = name.strip()
                    device_id = device_id.strip()
                    
                    item_id = tree.insert('', 'end', values=(str(index), name), tags=('item',))
                    tree.device_data[item_id] = {'id': device_id, 'original_name': name}
                    index += 1  # Incrementa o contador
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load devices: {str(e)}")
    
    # Apenas o botão de Confirm
    edit_btn = tk.Button(
        edit_frame, 
        text="Confirm", 
        command=on_edit,
        bg='#404040',
        fg='#ffffff',
        activebackground='#4a4a4a',
        activeforeground='#ffffff',
        relief='flat',
        font=('Segoe UI', 8),
        padx=2,
        pady=0,
        width=10,
        height=0
    )
    edit_btn.grid(row=0, column=1, padx=5)
    
    # Events
    tree.bind('<<TreeviewSelect>>', on_select)
    
    # Initial device load
    update_devices()
    
    return frame

def create_main_window():
    root = tk.Tk()
    root.title("Audio Device Name Editor")
    root.geometry("545x310")
    root.resizable(False, False)  # Torna a janela não redimensionável
    
    # Aplica o tema escuro
    style = set_dark_theme()
    
    # Configura cores do root
    root.configure(bg='#2b2b2b')
    
    # Força o tema escuro em todos os widgets
    root.option_add('*TCombobox*Listbox.background', '#333333')
    root.option_add('*TCombobox*Listbox.foreground', '#ffffff')
    root.option_add('*Background', '#3c3c3c')
    root.option_add('*Foreground', '#ffffff')
    root.option_add('*selectBackground', '#505050')
    root.option_add('*selectForeground', '#ffffff')
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)
    
    create_device_frame(main_frame)
    
    return root

if __name__ == "__main__":
    run_as_admin()
    root = create_main_window()
    root.mainloop()
