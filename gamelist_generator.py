#!/usr/bin/env python3
"""
GameList XML Generator
A GUI application to generate gamelist.xml files for ROM collections.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Set, Dict, Optional


class GameListGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("GameList XML Generator")
        self.root.geometry("800x600")
        
        # Variables
        self.rom_folder = tk.StringVar()
        self.image_folder = tk.StringVar()
        self.available_extensions = set()
        self.selected_extensions = set()
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # ROM Folder selection
        ttk.Label(main_frame, text="ROM Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.rom_folder, state="readonly").grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5
        )
        ttk.Button(main_frame, text="Browse", command=self.select_rom_folder).grid(
            row=0, column=2, padx=(5, 0), pady=5
        )
        
        # Image Folder selection
        ttk.Label(main_frame, text="Image Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.image_folder, state="readonly").grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5
        )
        ttk.Button(main_frame, text="Browse", command=self.select_image_folder).grid(
            row=1, column=2, padx=(5, 0), pady=5
        )
        
        # File Extensions section
        extensions_frame = ttk.LabelFrame(main_frame, text="File Extensions", padding="5")
        extensions_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        extensions_frame.columnconfigure(0, weight=1)
        
        # Extensions listbox with scrollbar
        listbox_frame = ttk.Frame(extensions_frame)
        listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.extensions_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=8)
        self.extensions_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.extensions_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.extensions_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = ttk.Frame(extensions_frame)
        buttons_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(buttons_frame, text="Select All", command=self.select_all_extensions).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Deselect All", command=self.deselect_all_extensions).grid(row=0, column=1, padx=5)
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready to generate gamelist.xml")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Generate button
        ttk.Button(main_frame, text="Generate gamelist.xml", command=self.generate_gamelist).grid(
            row=4, column=0, columnspan=3, pady=20
        )
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(2, weight=1)
        extensions_frame.rowconfigure(0, weight=1)
    
    def select_rom_folder(self):
        """Select the ROM folder and scan for file extensions"""
        folder = filedialog.askdirectory(title="Select ROM Folder")
        if folder:
            self.rom_folder.set(folder)
            self.scan_extensions(folder)
    
    def select_image_folder(self):
        """Select the image folder"""
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_folder.set(folder)
    
    def scan_extensions(self, folder_path: str):
        """Scan the selected folder for file extensions"""
        self.available_extensions.clear()
        self.extensions_listbox.delete(0, tk.END)
        
        try:
            for file_path in Path(folder_path).rglob('*'):
                if file_path.is_file() and file_path.suffix:
                    self.available_extensions.add(file_path.suffix.lower())
            
            # Sort and display extensions
            sorted_extensions = sorted(self.available_extensions)
            for ext in sorted_extensions:
                self.extensions_listbox.insert(tk.END, ext)
            
            self.progress_var.set(f"Found {len(sorted_extensions)} file extensions in the ROM folder")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scan folder: {str(e)}")
    
    def select_all_extensions(self):
        """Select all extensions in the listbox"""
        self.extensions_listbox.selection_set(0, tk.END)
    
    def deselect_all_extensions(self):
        """Deselect all extensions in the listbox"""
        self.extensions_listbox.selection_clear(0, tk.END)
    
    def get_selected_extensions(self) -> Set[str]:
        """Get the currently selected extensions"""
        selected_indices = self.extensions_listbox.curselection()
        selected_exts = set()
        for idx in selected_indices:
            selected_exts.add(self.extensions_listbox.get(idx))
        return selected_exts
    
    def generate_gamelist(self):
        """Generate the gamelist.xml file"""
        rom_folder = self.rom_folder.get()
        image_folder = self.image_folder.get()
        selected_extensions = self.get_selected_extensions()
        
        # Validation
        if not rom_folder:
            messagebox.showerror("Error", "Please select a ROM folder")
            return
        
        if not selected_extensions:
            messagebox.showerror("Error", "Please select at least one file extension")
            return
        
        try:
            # Ask where to save the gamelist.xml
            output_file = filedialog.asksaveasfilename(
                title="Save gamelist.xml",
                defaultextension=".xml",
                filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
                initialdir=rom_folder,
                initialfile="gamelist.xml"
            )
            
            if not output_file:
                return
            
            self.progress_var.set("Scanning files...")
            self.progress_bar['value'] = 0
            self.root.update()
            
            # Find all matching files
            matching_files = []
            processed_names = set()  # Prevent duplicates
            
            for file_path in Path(rom_folder).rglob('*'):
                if (file_path.is_file() and 
                    file_path.suffix.lower() in selected_extensions and
                    str(file_path) not in processed_names):
                    matching_files.append(file_path)
                    processed_names.add(str(file_path))
            
            if not matching_files:
                messagebox.showwarning("Warning", "No files found matching the selected extensions")
                return
            
            # Create XML structure
            root_elem = ET.Element("gameList")
            
            total_files = len(matching_files)
            for i, file_path in enumerate(matching_files):
                if i >= total_files:  # Safety check to prevent infinite loops
                    break
                    
                self.progress_var.set(f"Processing file {i+1}/{total_files}: {file_path.name}")
                self.progress_bar['value'] = (i / total_files) * 100
                self.root.update()
                
                game_elem = ET.SubElement(root_elem, "game")
                
                # Relative path from ROM folder
                relative_path = "./" + str(file_path.relative_to(Path(rom_folder)))
                ET.SubElement(game_elem, "path").text = relative_path
                
                # Game name (filename without extension)
                game_name = file_path.stem
                ET.SubElement(game_elem, "name").text = game_name
                
                # Image path (if image folder is specified)
                if image_folder:
                    # Look for matching image file
                    image_path = self.find_matching_image(file_path.stem, image_folder)
                    if image_path:
                        # Create relative path from ROM folder perspective
                        rom_folder_path = Path(rom_folder)
                        image_file_path = Path(image_path)
                        
                        try:
                            # Get the relative path from ROM folder to image file
                            relative_to_rom = image_file_path.relative_to(rom_folder_path)
                            relative_image_path = f"./{relative_to_rom}"
                        except ValueError:
                            # Fallback: use just the folder name and file name
                            image_folder_name = Path(image_folder).name
                            image_file_name = Path(image_path).name
                            relative_image_path = f"./{image_folder_name}/{image_file_name}"
                        
                        ET.SubElement(game_elem, "image").text = relative_image_path
                
                # Default empty fields (self-closing tags)
                releasedate_elem = ET.SubElement(game_elem, "releasedate")
                developer_elem = ET.SubElement(game_elem, "developer")
                publisher_elem = ET.SubElement(game_elem, "publisher") 
                genre_elem = ET.SubElement(game_elem, "genre")
                desc_elem = ET.SubElement(game_elem, "desc")
            
            # Write XML file
            self.progress_var.set("Writing XML file...")
            self.progress_bar['value'] = 100
            self.root.update()
            
            tree = ET.ElementTree(root_elem)
            ET.indent(tree, space="    ", level=0)  # Pretty print
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            self.progress_var.set(f"Successfully generated gamelist.xml with {total_files} games")
            messagebox.showinfo("Success", f"Generated gamelist.xml with {total_files} games\nSaved to: {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate gamelist.xml: {str(e)}")
            self.progress_var.set("Error occurred during generation")
        
        finally:
            self.progress_bar['value'] = 0
    
    def find_matching_image(self, game_name: str, image_folder: str) -> Optional[str]:
        """Find a matching image file for the given game name"""
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
        
        for ext in image_extensions:
            image_path = Path(image_folder) / f"{game_name}{ext}"
            if image_path.exists():
                return str(image_path)
        
        return None


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = GameListGenerator(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
