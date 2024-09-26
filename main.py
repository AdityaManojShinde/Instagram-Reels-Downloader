import instaloader
import os
import time
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

class InstagramReelDownloader:
    def __init__(self, session_id):
        self.session_id = session_id
        self.loader = instaloader.Instaloader()

    def download_reel(self, url, save_path, custom_name=None):
        try:
            shortcode = url.split('/')[-2]  # Extract shortcode from URL
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

            # Ensure that only video posts are downloaded
            if not post.is_video:
                raise RuntimeError("The provided URL does not point to a video reel.")

            # Download the post to a temporary folder (current directory)
            self.loader.download_post(post, target=shortcode)

            # Find the downloaded file
            for file in os.listdir(shortcode):
                if file.endswith('.mp4'):
                    src = os.path.join(shortcode, file)

                    # Use custom name if provided, else default to the original filename
                    reel_filename = f"{custom_name}.mp4" if custom_name else file
                    dest = os.path.join(save_path, reel_filename)
                    
                    # Move the file to the specified directory with the custom name
                    shutil.move(src, dest)

                    # Clean up the temporary folder
                    shutil.rmtree(shortcode)

                    return dest
            raise RuntimeError("Video reel not found after download.")
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

class InstagramReelDownloaderApp:
    def __init__(self, root, downloader):
        self.root = root
        self.downloader = downloader
        self.root.title("Python Instagram Reel Downloader by Aditya Shinde")
        self.root.geometry("500x400")  # Adjust window size for extra input
        self.root.configure(bg="white")  # Set background color
        self.create_widgets()

    def create_widgets(self):
        # Margin around widgets
        margin = 15

        tk.Label(self.root, text="Enter the Instagram reel URL:", bg="white").pack(pady=(margin, 5))
        self.url_entry = tk.Entry(self.root, width=60, font=('Arial', 12))
        self.url_entry.pack(pady=5, padx=margin)

        tk.Label(self.root, text="Select the directory to save the reel:", bg="white").pack(pady=(margin, 5))
        self.save_path_entry = tk.Entry(self.root, width=60, font=('Arial', 12))
        self.save_path_entry.pack(pady=5, padx=margin)
        
        browse_button = tk.Button(self.root, text="Browse", command=self.browse_directory, width=10)
        browse_button.pack(pady=(0, 10))

        tk.Label(self.root, text="Enter a custom name for the video (optional):", bg="white").pack(pady=(margin, 5))
        self.custom_name_entry = tk.Entry(self.root, width=60, font=('Arial', 12))
        self.custom_name_entry.pack(pady=5, padx=margin)

        download_button = tk.Button(self.root, text="Download", command=self.download_reel, width=15)
        download_button.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, directory)

    def download_reel(self):
        url = self.url_entry.get().strip()
        save_path = self.save_path_entry.get().strip()
        custom_name = self.custom_name_entry.get().strip()  # Get custom name

        if not url or not save_path:
            messagebox.showerror("Input Error", "Please provide both URL and save path.")
            return

        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                messagebox.showerror("Directory Error", f"Failed to create directory: {e}")
                return

        try:
            reel_filepath = self.downloader.download_reel(url, save_path, custom_name)
            messagebox.showinfo("Success", f"Downloaded Successfully: {reel_filepath}")
        except RuntimeError as e:
            messagebox.showerror("Download Error", str(e))

def main():
    # Replace with your actual Instagram session ID
    session_id = "Your Instagram Session ID Here"
    downloader = InstagramReelDownloader(session_id)

    root = tk.Tk()
    app = InstagramReelDownloaderApp(root, downloader)
    root.mainloop()

if __name__ == "__main__":
    main()
