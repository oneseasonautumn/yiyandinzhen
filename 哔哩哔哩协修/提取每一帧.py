import cv2
import os

def extract_all_frames(video_path, output_folder):
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Error: Cannot open video file.")
        return

    # Video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎞️ Total frames to extract: {total_frames}")

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        output_path = os.path.join(output_folder, f"frame_{frame_index:05d}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"✅ Saved: {output_path}")
        frame_index += 1

    cap.release()
    print("✅ Done. All frames extracted.")

# Example usage
if __name__ == "__main__":
    video_file = "C:/Users/User\Downloads/Telegram Desktop/30802579169-1-192.mp4"            # Path to your video
    output_folder = "all_frames"        # Output directory
    extract_all_frames(video_file, output_folder)
