import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont


class Diange:
    async def main(self, msg, nub):
        text = None

        if msg.raw_message == "点歌帮助":
            text = """点歌使用说明：
发送"点歌:歌名"搜索歌曲
发送"听:序号"播放对应歌曲
例如：点歌:周杰伦"""
            return {'try': 'text', "text": text, 'nub': nub}

        if str(msg.raw_message).startswith("点歌:"):
            song_name = msg.raw_message.split(":", 1)[1].strip()

            if not song_name:
                text = "请输入要搜索的歌曲名称"
                return {'try': 'text', "text": text, 'nub': nub}

            try:
                search_url = f'https://music.163.com/api/search/get/web?csrf_token=&s={requests.utils.quote(song_name)}&type=1&offset=0&total=true&limit=10'

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://music.163.com/"
                }

                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code != 200:
                    text = "搜索失败，请稍后重试"
                    return {'try': 'text', "text": text, 'nub': nub}

                data = response.json()

                if 'result' not in data or 'songs' not in data['result']:
                    text = "未找到相关歌曲"
                    return {'try': 'text', "text": text, 'nub': nub}

                song_list = data['result']['songs']

                if not song_list:
                    text = "未找到相关歌曲"
                    return {'try': 'text', "text": text, 'nub': nub}

                cache_data = []

                for idx, song_data in enumerate(song_list, 1):
                    song_name_result = song_data.get('name', '未知')
                    artists = song_data.get('artists', [])
                    artist_name = artists[0].get('name', '未知') if artists else '未知'
                    song_id = song_data.get('id', '')
                    album_name = song_data.get('album', {}).get('name', '未知')

                    cache_data.append({
                        'songId': song_id,
                        'songName': song_name_result,
                        'artist': artist_name,
                        'album': album_name
                    })

                user_id = str(msg.user_id)
                cache_file = f"plugins/ZhiZhangConee/mods/logs/diange_cache_{user_id}.json"

                os.makedirs(os.path.dirname(cache_file), exist_ok=True)

                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f, ensure_ascii=False)

                image_path = self.create_song_list_image(cache_data, song_name)

                result_text = f"搜索结果（共{len(song_list)}首）\n发送\"听:序号\"即可播放"

                return {'try': 'image', "text": image_path, 'nub': nub}

            except Exception as e:
                text = f"搜索出错：{str(e)}"
                return {'try': 'text', "text": text, 'nub': nub}

        if str(msg.raw_message).startswith("听:"):
            try:
                choice_str = msg.raw_message.split(":", 1)[1].strip()
                choice = int(choice_str) - 1

                user_id = str(msg.user_id)
                cache_file = f"plugins/ZhiZhangConee/mods/logs/diange_cache_{user_id}.json"

                if not os.path.exists(cache_file):
                    text = "请先使用\"点歌:歌名\"搜索歌曲"
                    return {'try': 'text', "text": text, 'nub': nub}

                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                if not cache_data:
                    text = "请先使用\"点歌:歌名\"搜索歌曲"
                    return {'try': 'text', "text": text, 'nub': nub}

                if choice < 0 or choice >= len(cache_data):
                    text = f"序号错误，请输入1-{len(cache_data)}之间的数字"
                    return {'try': 'text', "text": text, 'nub': nub}

                song_info = cache_data[choice]
                song_id = song_info['songId']

                url = f'https://music.163.com/song/media/outer/url?id={song_id}.mp3'
                print(url)

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://music.163.com/"
                }

                filename = "plugins/ZhiZhangConee/mods/logs/diange_music.mp3"
                filename2 = "/plugins/ZhiZhangConee/mods/logs/diange_music.mp3"

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                res = requests.get(url, headers=headers, timeout=30, allow_redirects=True)

                if res.status_code == 200 and len(res.content) > 1000:
                    with open(filename, 'wb') as f:
                        f.write(res.content)

                    text = f"正在播放：{song_info['songName']} - {song_info['artist']}"
                    return {'try': 'record', "text": filename2, 'nub': nub}
                else:
                    text = "歌曲暂无音源或版权受限，请尝试其他歌曲"
                    return {'try': 'text', "text": text, 'nub': nub}

            except ValueError:
                text = "请输入有效的序号"
                return {'try': 'text', "text": text, 'nub': nub}
            except Exception as e:
                text = f"播放出错：{str(e)}"
                return {'try': 'text', "text": text, 'nub': nub}

        return None

    def create_song_list_image(self, song_list, search_keyword):
        background_path = "data/5.jpg"

        output_path = "plugins/ZhiZhangConee/mods/logs/diange_result.png"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        img = Image.open(background_path)

        draw = ImageDraw.Draw(img)

        width, height = img.size

        try:
            title_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
            content_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
        except:
            try:
                title_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 36)
                content_font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", 28)
            except:
                title_font = ImageFont.load_default()
                content_font = ImageFont.load_default()

        title_text = f"搜索结果: {search_keyword}"

        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = (width - title_width) // 2
        title_y = 30

        shadow_offset = 2
        for offset_x, offset_y in [(-shadow_offset, -shadow_offset), (-shadow_offset, shadow_offset),
                                   (shadow_offset, -shadow_offset), (shadow_offset, shadow_offset)]:
            draw.text((title_x + offset_x, title_y + offset_y), title_text, font=title_font, fill=(0, 0, 0, 128))

        draw.text((title_x, title_y), title_text, font=title_font, fill=(255, 255, 255))

        line_height = 45
        start_y = title_y + 60

        for idx, song_info in enumerate(song_list, 1):
            song_text = f"{idx}. {song_info['songName']} - {song_info['artist']}"

            y_position = start_y + (idx - 1) * line_height

            if y_position > height - 50:
                break

            shadow_offset = 1
            for offset_x, offset_y in [(-shadow_offset, -shadow_offset), (-shadow_offset, shadow_offset),
                                       (shadow_offset, -shadow_offset), (shadow_offset, shadow_offset)]:
                draw.text((50 + offset_x, y_position + offset_y), song_text, font=content_font, fill=(0, 0, 0, 128))

            draw.text((50, y_position), song_text, font=content_font, fill=(255, 255, 255))

        footer_text = f"共 {len(song_list)} 首歌曲 | 发送\"听:序号\"播放"
        bbox_footer = draw.textbbox((0, 0), footer_text, font=content_font)
        footer_width = bbox_footer[2] - bbox_footer[0]
        footer_x = (width - footer_width) // 2
        footer_y = height - 40

        for offset_x, offset_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((footer_x + offset_x, footer_y + offset_y), footer_text, font=content_font, fill=(0, 0, 0, 128))

        draw.text((footer_x, footer_y), footer_text, font=content_font, fill=(255, 255, 255))

        img.save(output_path, "PNG")

        return output_path
