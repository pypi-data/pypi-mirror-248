import asyncio
from multiprocessing.shared_memory import SharedMemory
import numpy as np

from frames_depot.frames_depot import FramesDepot


if __name__ == "__main__":
    import cv2

    async def main():
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("/Volumes/Extreme SSD/CONDIVISA_ITALIC/14꞉15꞉56.14(A)PGM.mxf")

        frame_size = (
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            3,
        )
        frames_depot = FramesDepot(frame_size, "frame_depot")
        mem = SharedMemory("frame_depot")
        current_frame = 0
        while True:
            ret, frame = cap.read()
            if ret:
                frame_dict = {"frame_number": current_frame, "frame": frame}
                await frames_depot.enqueue(frame_dict)
                frames_depot.get_frame(current_frame)
                my_frame = np.ndarray(frame_size, dtype=np.uint8, buffer=mem.buf)
                cv2.imshow("frame", my_frame)
                cv2.waitKey(1)
                current_frame += 1
                print("=" * (10-len(frames_depot)), end="\r")
            else:
                await frames_depot.close()
                break

    asyncio.run(main())
