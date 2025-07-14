import cv2
import os

def resize_to_match(img, width, height):
    return cv2.resize(img, (width, height))

def get_frame_at_second(cap, second, fps):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(second * fps))
    ret, frame = cap.read()
    return frame if ret else None

def replace_first_frame_each_second(video_path, replacement_path, output_path):
    is_video = replacement_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Cannot open main video.")
        return

    main_fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(total_frames / main_fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, main_fps, (width, height))

    # Handle replacement source
    replacement_img = None
    replacement_video = None

    if is_video:
        replacement_video = cv2.VideoCapture(replacement_path)
        if not replacement_video.isOpened():
            print("❌ Cannot open replacement video.")
            return
        replacement_fps = replacement_video.get(cv2.CAP_PROP_FPS)
    else:
        replacement_img = cv2.imread(replacement_path)
        if replacement_img is None:
            print("❌ Cannot load replacement image.")
            return
        replacement_img = resize_to_match(replacement_img, width, height)

    current_frame = 0
    second_marker = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if int(current_frame) == int(second_marker * main_fps):
            if is_video:
                rep_frame = get_frame_at_second(replacement_video, second_marker, replacement_fps)
                if rep_frame is not None:
                    rep_frame = resize_to_match(rep_frame, width, height)
                    out.write(rep_frame)
                else:
                    out.write(frame)
            else:
                out.write(replacement_img)
            second_marker += 1
        else:
            out.write(frame)

        current_frame += 1

    cap.release()
    out.release()
    if replacement_video:
        replacement_video.release()

    print("\n✅ Done. Output saved to:", output_path)

# --- Main Program ---
if __name__ == "__main__":
    print("🎞 Replace First Frame of Every Second in Video")

    input_video = input("📥 Enter main video path: ").strip('" ')
    replacement_path = input("🎭 Enter replacement image or video path: ").strip('" ')
    output_video = input("💾 Enter output video path (e.g., output.mp4): ").strip('" ')

    replace_first_frame_each_second(input_video, replacement_path, output_video)
