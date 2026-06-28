---
title: "README"
output: html_document
date: "2026-06-28"
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

# Coral Photo Classifier

A web-based tool for classifying coral photos from underwater surveys. This app runs locally in your browser and helps you efficiently classify coral species, locations, and counts from camera trap images.

## Features

- 🔍 **Zoom functionality** - Left-click to zoom in, right-click to zoom out on photos
- ⌨️ **Keyboard shortcuts** - Fast classification with keyboard navigation
- 💾 **Auto-save** - Your progress is automatically saved in the browser
- 📝 **Autofill species** - Start typing to see previously used species names
- ⏮️ **Go back** - Easily navigate to previous photos to make corrections
-  **Progress tracking** - See how many photos you've classified

## Installation & Setup

### Step 1: Download Required Files

You need these files in the same folder:
1. `index.html` - The main application
2. `papaparse.min.js` - CSV parsing library (download from [here](https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js))
3. Your CSV file with photo metadata
4. Your photo folder

### Step 2: Organize Your Files

Your folder structure should look like this:

```text
your_project_folder/
├── index.html
├── papaparse.min.js
├── your_csv_file.csv
└── camera_offload_folder/
    ├── P2050001.JPG
    ├── P2050002.JPG
    └── ...
```

### Step 3: Start the Local Server

**Important:** You cannot just double-click `index.html`. You must run a local server.

#### On macOS:

1. Open **Terminal** (Cmd + Space, type "Terminal")
2. Navigate to your folder:
   ```bash
   cd /path/to/your/folder
   ```
   *(Tip: Type `cd ` then drag your folder into Terminal)*
3. Start the server:
   ```bash
   python3 -m http.server 8000
   ```

#### On Windows:

1. Open **File Explorer** and navigate to your folder
2. Click in the address bar, type `cmd`, and press Enter
3. Start the server:
   ```cmd
   python -m http.server 8000
   ```
   *(If that doesn't work, try `python3 -m http.server 8000`)*

#### On Linux:

```bash
cd /path/to/your/folder
python3 -m http.server 8000
```

### Step 4: Open the Application

Open your web browser and go to:

```text
http://localhost:8000/index.html
```

## Usage Guide

### Initial Setup

1. **Enter your name** - This will be recorded in the "Classified by" column
2. **Photo Folder Path** (optional) - If your photos are in a subfolder, enter the folder name here. Leave blank if photos are in the same folder as `index.html`
3. **Upload CSV** - Click the upload area and select your CSV file

### Classifying Photos

For each photo, fill in:

- **Coral Location** - Click a button or press the corresponding key:
  - **R** - On prop root
  - **U** - Under prop roots
  - **M** - 1 m out from prop roots
  - **D** - Under dead mangrove material
  - **B** - > 1 m out / within bays

- **Species** - Start typing to see autofill suggestions from previously classified photos. Use arrow keys to navigate and Enter to select

- **Count** - Number of coral colonies (defaults to 1)

### Navigation Controls

- **Save ➡️** or **Enter** - Save and move to next photo
- **️ Previous** - Go back to the previous photo
- **Skip** - Skip this photo without classifying
- **Archive** - Mark photo as duplicate or unusable

### Image Zoom

- **Left-click** on the image to zoom in (click multiple times to zoom further)
- **Right-click** to zoom out
- Zoom resets when you move to the next photo

### Saving Your Work

- **Auto-save**: Your progress is automatically saved in your browser after each photo
- **Manual save**: Click **💾 Save Progress** to download a CSV file with your current progress
- **Final download**: When finished, click **⬇️ Download Final CSV** to get your completed classification file

### Resuming Work

If you need to continue later:
1. Open the app again
2. Upload your previously saved "PROGRESS" CSV file (not the original blank one)
3. The app will automatically skip already-classified photos and pick up where you left off

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Enter** | Save and go to next photo |
| **← (Left Arrow)** | Go to previous photo |
| **R, U, M, D, B** | Select coral location |
| **↑/↓ (Arrow keys)** | Navigate species dropdown (when typing) |

## Troubleshooting

### "Image not found" error
- Verify the folder path is correct
- Check that photos exist in the specified folder
- Try leaving the folder path blank if photos are in the same folder as `index.html`
- Make sure you're using forward slashes (`/`) not backslashes (`\`)

### "404 File not found" when opening the app
- Ensure `index.html` is in the folder where you started the server
- Verify the URL is exactly: `http://localhost:8000/index.html`
- Check that the server is still running in Terminal/Command Prompt

### Server won't start
- Make sure Python is installed (check by typing `python --version` or `python3 --version`)
- Try using `python` instead of `python3` or vice versa
- Make sure port 8000 isn't already in use

### Browser won't load photos
- **Don't double-click `index.html`** - you must use the server method
- Make sure `papaparse.min.js` is in the same folder as `index.html`
- Check browser console for errors (F12 → Console tab)

## Tips for Efficient Classification

1. **Use keyboard shortcuts** - Keep your hands on the keyboard for faster classification
2. **Type species names** - The app remembers what you've typed before, so you only need to type the first few letters
3. **Zoom in for small corals** - Left-click to zoom in on small or hard-to-see corals
4. **Don't worry about mistakes** - Use the Previous button to go back and fix errors
5. **Save progress regularly** - Download your progress CSV periodically as a backup

## File Format

The app works with CSV files containing these columns:
- `Filename` - Photo filename (e.g., P2050001)
- `Date` - Survey date
- `Lat` - Latitude
- `Lon` - Longitude
- `Species` - Coral species (filled by app)
- `Count` - Number of colonies (filled by app)
- `Location` - Coral location code (filled by app)
- `Classified by` - Classifier name (filled by app)

## Support

If you encounter any issues or have questions, please contact the project maintainer.

---

**Note:** This app runs entirely in your browser - no data is sent to external servers. All your work stays on your computer.