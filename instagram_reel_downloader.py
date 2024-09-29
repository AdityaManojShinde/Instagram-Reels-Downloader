import instaloader
import os
import shutil
from gooey import Gooey, GooeyParser

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

@Gooey(program_name="Instagram Reel Downloader", default_size=(600, 500))
def main():
    parser = GooeyParser(description="Download Instagram Reels Easily")
    
    parser.add_argument(
        'url', 
        metavar='Instagram Reel URL', 
        help="Enter the URL of the Instagram reel",
        widget='TextField'
    )
    
    parser.add_argument(
        'save_path', 
        metavar='Save Directory', 
        help="Select the directory to save the reel",
        widget='DirChooser'
    )
    
    parser.add_argument(
        '--custom_name', 
        metavar='Custom Name (optional)', 
        help="Enter a custom name for the downloaded video (optional)", 
        default='', 
        widget='TextField'
    )

    args = parser.parse_args()
    
    session_id = "Your Instagram Session ID Here"  # Replace with your actual session ID
    downloader = InstagramReelDownloader(session_id)

    try:
        reel_filepath = downloader.download_reel(args.url, args.save_path, args.custom_name)
        print(f"Downloaded Successfully: {reel_filepath}")
    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


