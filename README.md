# Audio Device Name Editor

A minimalist Windows application to edit audio device friendly names with a dark-themed interface.

## Features

- List all connected audio devices
- Edit device friendly names
- Dark mode interface
- Clean and simple design
- Mouse wheel scrolling support

## Screenshots

[Add your screenshots here]

## Requirements

- Windows OS
- Python 3.x
- Administrator privileges (required to edit device names)

## Installation

1. Clone this repository:
 git clone https://github.com/yourusername/audio-device-name-editor.git

## Usage

1. Launch the application (it will automatically request administrator privileges)
2. The application will display a list of all parent devices connected to your computer
3. Select a device from the list
4. Enter the new name in the text box
5. Click "Confirm" to apply the changes
6. Restart Windows

## Technical Details

- Built with Python and Tkinter
- Uses PowerShell commands to interact with Windows device management
- Requires administrator privileges to modify device names
- Custom dark theme implementation
- Minimalist design with no unnecessary UI elements

## Known Limitations

- Windows only
- Requires restart to apply changes
- Must be run with administrator privileges

## Contributing

Feel free to open issues or submit pull requests with improvements.

## Acknowledgments

- Inspired by the need for a simple audio device name editor because I couldn't find any other that was simple and easy to use. And because Warframe is weird to mess with the audio device names when you have multiple from the same manufacturer.