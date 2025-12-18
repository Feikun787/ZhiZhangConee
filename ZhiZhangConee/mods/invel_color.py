# invel_color.py
import re
import requests
from PIL import Image, ImageSequence
import io
import os
import uuid
import numpy as np

class InveColor:

    async def invecolor(self, msg, nub):
        pattern = r"CQ:reply,id=(\d+)](.+)"
        match = re.search(pattern, msg.raw_message)
        if match:
            id = match.group(1)
            print(id)
            print(msg)
            message = match.group(2)
            if message in ['图片反转', '视频反转']:
                a = await self.api.get_msg(id)
                print(a)
                print(type(a))
                url = (str(a).split('url="')[-1].split('"')[0])
                filename = str(a).split('file="')[-1].split('"')[0]
                extension = filename.split('.')[-1]
                data = requests.get(url)

                # 生成唯一标识符以避免文件名冲突
                unique_id = str(uuid.uuid4())
                original_file_path = f"plugins/ZhiZhangConee/data/1.{extension}"

                with open(original_file_path, "wb") as f:
                    f.write(data.content)

                # 判断是图片还是视频
                if message == '图片反转':
                    self.invert_image_bytes(original_file_path, extension)
                    return {'try': 'image', 'text': original_file_path, 'nub': nub}
                elif message == '视频反转':
                    output_path = f"plugins/ZhiZhangConee/data/2.mp4"
                    self.invert_video_colors(original_file_path, output_path)
                    return {'try': 'video', 'text': output_path, 'nub': nub}
        return None

    def invert_image_bytes(self, file_path, extension):
        """
        反转图片的颜色，支持动图。
        :param file_path: 图片文件路径
        :param extension: 图片格式后缀
        """
        with open(file_path, 'rb') as f:
            image_bytes = f.read()
            image = Image.open(io.BytesIO(image_bytes))

            try:
                image.seek(1)
                is_animated = True
                image.seek(0)
            except EOFError:
                is_animated = False

            if is_animated:
                frames = []
                durations = []
                disposals = []

                for frame in ImageSequence.Iterator(image):
                    durations.append(frame.info.get('duration', 100))
                    disposals.append(frame.info.get('disposal', 2))

                    if frame.mode in ("RGBA", "P"):
                        frame = frame.convert("RGBA")
                        r, g, b, a = frame.split()
                        rgb_image = Image.merge("RGB", (r, g, b))
                        inverted_rgb = Image.eval(rgb_image, lambda p: 255 - p)
                        inverted_frame = Image.merge("RGBA", inverted_rgb.split() + (a,))
                    elif frame.mode == "RGB":
                        inverted_frame = Image.eval(frame, lambda p: 255 - p)
                    elif frame.mode == "L":
                        inverted_frame = Image.eval(frame, lambda p: 255 - p)
                    else:
                        inverted_frame = Image.eval(frame, lambda p: 255 - p)

                    frames.append(inverted_frame)

                frames[0].save(
                    file_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=image.info.get('loop', 0),
                    disposal=disposals,
                    format='GIF'
                )
            else:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGBA")
                    r, g, b, a = image.split()
                    rgb_image = Image.merge("RGB", (r, g, b))
                    inverted_rgb = Image.eval(rgb_image, lambda p: 255 - p)
                    inverted_image = Image.merge("RGBA", inverted_rgb.split() + (a,))
                elif image.mode == "RGB":
                    inverted_image = Image.eval(image, lambda p: 255 - p)
                elif image.mode == "L":
                    inverted_image = Image.eval(image, lambda p: 255 - p)
                else:
                    inverted_image = Image.eval(image, lambda p: 255 - p)

                inverted_bytes = io.BytesIO()
                inverted_image.save(inverted_bytes, format=image.format)
                with open(file_path, 'wb') as f:
                    f.write(inverted_bytes.getvalue())

    def invert_video_colors(self, input_path, output_path):
        """
        使用OpenCV反转视频颜色
        :param input_path: 输入视频路径
        :param output_path: 输出视频路径
        """
        try:
            import cv2

            # 检查文件是否存在且不为空
            if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
                raise FileNotFoundError("输入视频文件不存在或为空")

            # 打开视频文件
            cap = cv2.VideoCapture(input_path)

            # 检查视频是否成功打开
            if not cap.isOpened():
                raise ValueError("无法打开视频文件")

            # 获取视频属性
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # 检查视频属性是否有效
            if fps <= 0 or width <= 0 or height <= 0:
                raise ValueError("视频文件属性无效")

            # 创建视频写入对象
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                # 反转颜色 (BGR格式)
                inverted_frame = 255 - frame

                # 写入处理后的帧
                out.write(inverted_frame)

            # 检查是否有成功处理的帧
            if frame_count == 0:
                raise ValueError("视频文件没有有效的帧数据")

            print(f"成功处理了 {frame_count} 帧")

            # 释放资源
            out.release()

        except Exception as e:
            print(f"视频处理失败: {e}")
            # 如果处理失败，复制原始文件
            try:
                import shutil
                shutil.copy2(input_path, output_path)
            except Exception as copy_error:
                print(f"复制文件也失败了: {copy_error}")



