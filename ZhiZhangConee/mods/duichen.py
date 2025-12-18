import re
import requests
from PIL import Image, ImageSequence
import io


class Duichen:

    async def duichen(self, msg, nub):
        # 修改 duichen 方法中的正则表达式
        pattern = r"CQ:reply,id=(\d+)](.+)"
        match = re.search(pattern, msg.raw_message)

        if match:
            id = match.group(1)
            message = match.group(2).strip()

            # 解析对称方式
            symmetries = {
                '上对称': 'top',
                '下对称': 'bottom',
                '左对称': 'left',
                '右对称': 'right',
                '旋转': 'kaleidoscope'  # 添加这一项
            }

            symmetry_type = None
            for key, value in symmetries.items():
                if message == key:
                    symmetry_type = value
                    break

            if symmetry_type:
                a = await self.api.get_msg(id)
                print(a)
                url = (str(a).split('url="')[-1].split('"')[0])
                print(url)
                geshi = str(a).split('file="')[-1].split('"')[0].split('.')[-1]
                data = requests.get(url)
                with open(r"plugins/ZhiZhangConee/data/1." + geshi, "wb") as f:
                    f.write(data.content)
                    f.close()
                self.symmetry_image_bytes(geshi, symmetry_type)
                return {'try': 'image', 'text': f'plugins/ZhiZhangConee/data/1.{geshi}', 'nub': nub}
        return None

    def symmetry_image_bytes(self, geshi, symmetry_type):
        """
        对图片进行对称处理，支持动图。
        :param geshi: 图片格式后缀
        :param symmetry_type: 对称类型 (top, bottom, left, right)
        """

        with open(r'plugins/ZhiZhangConee/data/1.' + geshi, 'rb') as f:
            image_bytes = f.read()
            image = Image.open(io.BytesIO(image_bytes))

            # 检查是否为动图
            try:
                image.seek(1)
                is_animated = True
                image.seek(0)
            except EOFError:
                is_animated = False

            if is_animated:
                # 处理动图
                frames = []
                durations = []
                disposals = []

                for frame in ImageSequence.Iterator(image):
                    durations.append(frame.info.get('duration', 100))
                    disposals.append(frame.info.get('disposal', 2))

                    # 处理当前帧的对称
                    processed_frame = self.apply_symmetry(frame.copy(), symmetry_type)
                    frames.append(processed_frame)

                # 保存动图为 GIF 格式
                frames[0].save(
                    r'plugins/ZhiZhangConee/data/1.' + geshi,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=image.info.get('loop', 0),
                    disposal=disposals,
                    format='GIF'
                )
            elif symmetry_type == 'kaleidoscope':
                result_image = self.kaleidoscope_effect(image)
                result_bytes = io.BytesIO()
                result_image.save(result_bytes, format='PNG')
                with open(r'plugins/ZhiZhangConee/data/1.' + geshi, 'wb') as f:
                    f.write(result_bytes.getvalue())
            else:
                # 处理静态图片
                result_image = self.apply_symmetry(image, symmetry_type)
                result_bytes = io.BytesIO()
                result_image.save(result_bytes, format=image.format)
                with open(r'plugins/ZhiZhangConee/data/1.' + geshi, 'wb') as f:
                    f.write(result_bytes.getvalue())


    def apply_symmetry(self, image, symmetry_type):
        """
        应用对称变换到单个图像
        :param image: PIL图像对象
        :param symmetry_type: 对称类型
        :return: 处理后的图像
        """
        # 确保图片模式兼容
        if image.mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGBA")

        width, height = image.size

        if symmetry_type == 'left':
            # 左对称：保留左侧部分，镜像到右侧
            left_half = image.crop((0, 0, width // 2, height))
            right_half = left_half.transpose(Image.FLIP_LEFT_RIGHT)
            result = Image.new(image.mode, (width, height))
            result.paste(left_half, (0, 0))
            result.paste(right_half, (width // 2, 0))
            return result

        elif symmetry_type == 'right':
            # 右对称：保留右侧部分，镜像到左侧
            right_half = image.crop((width // 2, 0, width, height))
            left_half = right_half.transpose(Image.FLIP_LEFT_RIGHT)
            result = Image.new(image.mode, (width, height))
            result.paste(left_half, (0, 0))
            result.paste(right_half, (width // 2, 0))
            return result

        elif symmetry_type == 'top':
            # 上对称：保留上半部分，镜像到下半部分
            top_half = image.crop((0, 0, width, height // 2))
            bottom_half = top_half.transpose(Image.FLIP_TOP_BOTTOM)
            result = Image.new(image.mode, (width, height))
            result.paste(top_half, (0, 0))
            result.paste(bottom_half, (0, height // 2))
            return result

        elif symmetry_type == 'bottom':
            # 下对称：保留下半部分，镜像到上半部分
            bottom_half = image.crop((0, height // 2, width, height))
            top_half = bottom_half.transpose(Image.FLIP_TOP_BOTTOM)
            result = Image.new(image.mode, (width, height))
            result.paste(top_half, (0, 0))
            result.paste(bottom_half, (0, height // 2))
            return result

        return image

    def kaleidoscope_effect(self, image, rings=8):
        """
        创建万花筒效果 - 缩小图片一圈圈围绕中心
        :param image: PIL图像对象
        :param rings: 圈数
        :return: 处理后的万花筒图像
        """
        # 确保图片是正方形，如果不是则裁剪成正方形
        width, height = image.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        image = image.crop((left, top, left + size, top + size))

        # 调整图像大小以便处理
        target_size = min(size, 400)
        image = image.resize((target_size, target_size), Image.LANCZOS)

        # 确保图片模式兼容
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA")

        # 创建输出图像
        output = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))

        # 计算每圈的缩放比例和旋转角度
        center = (target_size // 2, target_size // 2)

        for i in range(rings):
            # 计算当前圈的缩放因子
            scale_factor = 1.0 - (i * 0.3 / rings)  # 每圈缩小一定比例
            if scale_factor <= 0:
                scale_factor = 0.1

            # 计算当前圈的旋转角度
            rotation_angle = i * (360 / rings)

            # 缩放图像
            new_size = int(target_size * scale_factor)
            if new_size <= 0:
                new_size = 1

            scaled_image = image.resize((new_size, new_size), Image.LANCZOS)

            # 旋转图像
            rotated_image = scaled_image.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)

            # 计算放置位置（居中）
            rot_width, rot_height = rotated_image.size
            x = center[0] - rot_width // 2
            y = center[1] - rot_height // 2

            # 将图像粘贴到输出图像上
            output.paste(rotated_image, (x, y), rotated_image if 'A' in rotated_image.mode else None)

        # 转换回原图像模式
        if image.mode != "RGBA":
            output = output.convert(image.mode)

        return output

    def add_kaleidoscope_to_symmetry_methods(self):
        """
        在对称方式字典中添加万花筒选项
        """
        # 在 duichen 方法中的 symmetries 字典里添加:
        # '万花筒': 'kaleidoscope'
        pass



