import threading

import audio
import head_pose
import detection
import threading as th

global cheat_count

exit_flag = th.Event()


def set_exit_status():
    exit_flag.set()


if __name__ == "__main__":
    # main()


    head_pose_thread = th.Thread(target=head_pose.pose)
    audio_thread = th.Thread(target=audio.sound)
    detection_thread = th.Thread(target=detection.run_detection)

    head_pose_thread.start()
    audio_thread.start()
    detection_thread.start()

    print("===========================================")
    print(detection.cheat_count)
    print("===========================================")

    if detection.cheat_count > 3:
        exit_flag.set()  # Set the exit flag to signal threads to exit

    head_pose_thread.join()
    audio_thread.join()
    detection_thread.join()
