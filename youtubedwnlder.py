import tkinter as tk
from tkinter import messagebox
from pytube import YouTube

def download_video(resolution):
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL")
        return

    try:
        yt = YouTube(url)
        stream = None
        if resolution == "high":
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res="1080p").first()
            if not stream:  # Fallback for high resolution
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif resolution == "low":
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res="360p").first()
            if not stream:  # Fallback for low resolution
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
        elif resolution == "audio":
            stream = yt.streams.filter(only_audio=True).first()

        if stream:
            stream.download(output_path=".")
            messagebox.showinfo("Success", f"{resolution.capitalize()} download completed!")
        else:
            messagebox.showerror("Error", f"{resolution.capitalize()} resolution not available for this video.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

# Enable right-click options for the entry field
def enable_right_click(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Cut", command=lambda: url_entry.event_generate("<<Cut>>"))
    menu.add_command(label="Copy", command=lambda: url_entry.event_generate("<<Copy>>"))
    menu.add_command(label="Paste", command=lambda: url_entry.event_generate("<<Paste>>"))
    menu.tk_popup(event.x_root, event.y_root)

def close_menu(event):
    try:
        menu.unpost()
    except:
        pass

url_label = tk.Label(root, text="Enter YouTube Video link here:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
url_entry.bind("<Button-3>", enable_right_click)
url_entry.bind("<FocusOut>", close_menu)

high_res_button = tk.Button(root, text="1080p Resolution", command=lambda: download_video("high"))
high_res_button.pack(pady=5)

low_res_button = tk.Button(root, text="360p Resolution", command=lambda: download_video("low"))
low_res_button.pack(pady=5)

audio_button = tk.Button(root, text="Sound Only", command=lambda: download_video("audio"))
audio_button.pack(pady=5)

# Run the main loop
root.mainloop()
