# GameList XML Generator

A GUI application to generate `gamelist.xml` files for ROM collections on Linux.

## Features

- **ROM Folder Selection**: Browse and select your ROM directory
- **Dynamic File Extension Detection**: Automatically detects all file extensions in the ROM folder
- **Selective File Filtering**: Choose which file extensions to include in the gamelist
- **Image Path Support**: Optionally specify an image folder to automatically link game images
- **Progress Tracking**: Real-time progress display during generation
- **Cross-platform GUI**: Works on Linux with X11 or Wayland

## Requirements

- Python 3.6 or higher
- tkinter (usually comes with Python)
- No additional dependencies required!

## Installation

1. Clone or download this repository
2. Make the script executable:
   ```bash
   chmod +x gamelist_generator.py
   ```

## Usage

### Running the Application

```bash
python3 gamelist_generator.py
```

Or directly:
```bash
./gamelist_generator.py
```

### Step-by-Step Guide

1. **Select ROM Folder**: Click "Browse" next to "ROM Folder" and choose your directory containing ROM files
2. **Choose File Extensions**: After selecting the ROM folder, the application will scan and display all file extensions found. Select the ones you want to include in your gamelist
3. **Select Image Folder** (Optional): If you have a separate folder with game images, browse and select it. The application will try to match images with ROM files by name
4. **Generate**: Click "Generate gamelist.xml" and choose where to save the output file

### Generated XML Structure

The application generates XML files compatible with EmulationStation and similar frontends:

```xml
<?xml version="1.0"?>
<gamelist>
    <game>
        <path>./GameTitle.zip</path>
        <name>Game Title</name>
        <image>./images/GameTitle.png</image>
        <releasedate></releasedate>
        <developer></developer>
        <publisher></publisher>
        <genre></genre>
        <desc></desc>
    </game>
</gamelist>
```

### Image Matching

If you specify an image folder, the application will automatically look for images with the same name as your ROM files (without extension) in these formats:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

## Example Workflow

1. You have ROMs in `/home/user/roms/snes/` with files like:
   - `Super Mario World.smc`
   - `The Legend of Zelda - A Link to the Past.sfc`
   - `Donkey Kong Country.zip`

2. You have images in `/home/user/images/snes/` with files like:
   - `Super Mario World.png`
   - `The Legend of Zelda - A Link to the Past.jpg`

3. The application will generate a gamelist.xml with proper paths and matched images.

## Customization

The generated XML includes empty fields for additional metadata (release date, developer, publisher, genre, description) that you can fill in manually or with other tools.

## Troubleshooting

- **GUI not appearing**: Make sure you have a display server running (X11 or Wayland) and the DISPLAY environment variable is set
- **Permission errors**: Ensure you have read access to the ROM folder and write access to the output location
- **No extensions found**: Make sure your ROM folder contains files with extensions

## License

This project is open source and available under the MIT License.
