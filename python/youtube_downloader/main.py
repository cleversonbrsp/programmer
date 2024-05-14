from pytube import YouTube

# Function to download YouTube video
def download_video(url, output_path='D:\VIDEOS'):
    try:
        yt = YouTube(url)
        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading '{yt.title}'...")
        stream.download(output_path)
        print('Download completed successfully!')
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
