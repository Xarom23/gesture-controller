# Human Gesture Control System

Computer vision and AI-based interface control system using hand and facial gestures. Enables mouse and keyboard control through natural hand movements and eye blinks.

## Description

This system was developed to explore the use of artificial intelligence and computer vision for interface control through human gestures. It aims to provide a more natural and intuitive way of interaction between users and computers, facilitating access and improving the user experience.

**Version:** 1.0
**Developed by:** Omar Luna Hernández
**License:** Free Software

## Features

### Hand Control
- **Mouse Mode**: Move cursor with hand position
- **Keyboard Mode**: Directional control via gestures (arrow keys: up, down, left, right)
- Independent configuration for left and right hands
- Detection of up to 2 hands simultaneously

### Facial Control
- **Left Eye Blink**: Left or right mouse click (configurable)
- **Right Eye Blink**: Right or left mouse click (configurable)
- Detection using Eye Aspect Ratio (EAR) calculation

### Graphical Interface
- Real-time video feed visualization
- Show/hide landmarks option
- Configuration panel with intuitive visual interface
- Quick mode switching
- Gesture control activation/deactivation

## Requirements

### Python
- Python 3.12 or higher

### Dependencies
See [requirements.txt](requirements.txt) for full list:
```
opencv-python>=4.9.0
mediapipe>=0.10.21
pyautogui>=0.9.54
Pillow>=10.0.0
numpy>=1.26.0
tkinter (included with Python)
```

### Development Dependencies
```
pytest>=9.0.0
pytest-cov>=7.0.0
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Codigo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Or install manually:
```bash
pip install opencv-python mediapipe pyautogui Pillow numpy
```

## Usage

### Run the Application
```bash
python main.py
```

### Configuration

The application uses a `config.json` file to store preferences:

```json
{
  "left_hand_mode": "keyboard",
  "right_hand_mode": "mouse",
  "left_blink_mode": "left_click",
  "right_blink_mode": "right_click"
}
```

#### Configuration Options:
- **left_hand_mode / right_hand_mode**: `"keyboard"` or `"mouse"`
- **left_blink_mode / right_blink_mode**: `"left_click"` or `"right_click"`

### Interface Controls

#### View Menu
- **View video**: Show/hide video feed
- **View reference points**: Show/hide detected landmarks

#### Options Menu
- **Configuration**: Open configuration panel
- **Enable/Disable gesture control**: Enable or disable gesture-based control

#### Help Menu
- **About**: Application information

## System Architecture

### Main Modules

#### [main.py](main.py)
Application entry point. Initializes the main graphical interface.

#### [principal.py](principal.py)
Main application window with:
- Canvas for video visualization
- Navigation menus
- Camera handler integration

#### [camera_handler.py](camera_handler.py)
Manages video capture and processing:
- Camera initialization
- Frame processing
- Coordination between detection and control

#### [landmark_detector.py](landmark_detector.py)
Landmark detection using MediaPipe:
- Hand detection (up to 2 hands)
- Facial mesh detection
- Container classes: `HandsResults`, `FaceResults`, `DetectionsResults`

#### [gesture_controller.py](gesture_controller.py)
Main system orchestrator:
- Processes hand and facial gestures
- Coordinates detection with simulation
- Dynamic configuration loading

#### [blink_detector.py](blink_detector.py)
Blink detection using Eye Aspect Ratio (EAR):
- Independent left and right eye detection
- Configurable threshold (default: 0.40)
- Algorithm based on 3D Euclidean distance using numpy
- Uses 6 key landmarks per eye for accurate detection

#### [trajectory_detector.py](trajectory_detector.py)
Trajectory detection for directional control:
- Detects movement in 4 cardinal directions
- Configurable movement threshold
- Coordinate normalization

#### [mouse_simulator.py](mouse_simulator.py)
Mouse event simulation:
- Cursor movement with normalized coordinates
- Left and right click
- Movement smoothing support

#### [keyboard_simulator.py](keyboard_simulator.py)
Keyboard event simulation:
- Key presses via PyAutoGUI
- Directional control (arrow keys)

#### [settings.py](settings.py)
Configuration interface:
- GUI with visual icons
- Mode switching
- Persistence to `config.json`

#### [about.py](about.py)
"About" window with project information.

#### [config.py](config.py)
Global configuration for colors and control variables.

## Testing

The project includes a comprehensive suite of unit and integration tests.

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov

# Generate HTML report
pytest --cov --cov-report=html
```

### Test Structure
```
test/
├── conftest.py              # Fixture configuration
├── test_blink_detector.py   # Blink detection tests
├── test_camera_handler.py   # Camera handler tests
├── test_gesture_controller.py  # Gesture controller tests
├── test_keyboard_simulator.py  # Keyboard simulator tests
├── test_landmark_detector.py   # Landmark detection tests
├── test_mouse_simulator.py     # Mouse simulator tests
├── test_trajectory_detector.py # Trajectory detection tests
└── test_integration.py         # Integration tests
```

### Coverage Configuration

See [.coveragerc](.coveragerc) for coverage configuration details. GUI files (Tkinter) are excluded from coverage analysis.

## Project Structure

```
Codigo/
├── assets/                  # Graphical resources
│   ├── keyboard.png
│   ├── left_click.png
│   ├── mouse_movement.png
│   └── right_click.png
├── test/                    # Test suite
│   └── *.py
├── main.py                  # Entry point
├── principal.py             # Main window
├── camera_handler.py        # Camera handler
├── landmark_detector.py     # Landmark detection
├── gesture_controller.py    # Gesture control
├── blink_detector.py        # Blink detection
├── trajectory_detector.py   # Trajectory detection
├── mouse_simulator.py       # Mouse simulation
├── keyboard_simulator.py    # Keyboard simulation
├── settings.py              # Configuration GUI
├── about.py                 # "About" window
├── config.py                # Global configuration
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── .coveragerc              # Coverage configuration
├── .gitignore               # Git ignored files
└── README.md                # This file
```

## Technologies Used

- **Python 3.12**: Main language
- **OpenCV**: Image and video processing
- **MediaPipe**: Face and hand landmark detection
- **PyAutoGUI**: Mouse and keyboard event simulation
- **Tkinter**: Graphical user interface
- **PIL/Pillow**: Image processing for GUI
- **pytest**: Testing framework

## Contributing

This is a thesis project. For questions or suggestions, please contact the developer.

## Credits

Developed by Omar Luna Hernández as part of a thesis project exploring the use of AI and computer vision for gestural control interfaces.

## Technical Notes

### Blink Detection Algorithm

The system uses the Eye Aspect Ratio (EAR) to detect blinks:

```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```

Where:
- `p1, p4`: Horizontal corners of the eye
- `p2, p3`: Upper eyelid vertical points
- `p5, p6`: Lower eyelid vertical points
- `|| ||`: Euclidean distance (3D using numpy)

**Eye Landmarks Used:**
- Right Eye: `[33, 159, 158, 133, 153, 145]`
- Left Eye: `[362, 380, 374, 263, 386, 385]`

When the eye is open, the EAR is relatively constant (~0.5-0.6). During a blink, the EAR drops significantly below the threshold (default: 0.40).

### Trajectory Detection

The system tracks the position of specific landmarks (e.g., index finger tip) and calculates displacement to determine movement direction. The configurable movement threshold (default: 60 pixels) prevents spurious detections.

### Real-time Configuration

The application monitors the `config.json` file and automatically reloads the configuration when changes are detected, allowing adjustments without restarting the application.

## Test Results

The project maintains **100% code coverage** with 108 tests:

| Module | Lines | Coverage | Tests |
|--------|-------|----------|-------|
| blink_detector.py | 28 | 100% | 9 |
| trajectory_detector.py | 33 | 100% | 13 |
| mouse_simulator.py | 15 | 100% | 8 |
| keyboard_simulator.py | 5 | 100% | 6 |
| landmark_detector.py | 48 | 100% | 17 |
| gesture_controller.py | 79 | 100% | 16 |
| camera_handler.py | 81 | 100% | 15 |
| **Integration** | - | - | 15 |
| **TOTAL** | **301** | **100%** | **108** |
