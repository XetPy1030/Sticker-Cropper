from telethon import TelegramClient, events
import os
from PIL import Image


folder = 'cropped_stickers (copysend)'
need_width = 512
need_height = 512

folder = 'temp'
need_width = 100
need_height = 100


def collect_all_images():
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            images.append(os.path.join(root, file))
    return images


def reformat_images(images):
    """
    Преобразует в 512x512 PNG,
    Сохраняет пропорции заполняя пустые места прозрачным фоном
    """
    for num, image in enumerate(images):
        print(f"Reformatting image {num} of {len(images)}")
        im = Image.open(image)
        width = im.size[0]
        height = im.size[1]
        if width > height:
            im = im.resize((need_width, int(need_height * height / width)))
        else:
            im = im.resize((int(need_width * width / height), need_height))

        new_im = Image.new("RGBA", (need_width, need_height), (0, 0, 0, 0))
        new_im.paste(im, ((need_width - im.size[0]) // 2, (need_height - im.size[1]) // 2))
        new_im.save(image, "PNG")


images = collect_all_images()
reformat_images(images)



#
#
# with TelegramClient('name', api_id, api_hash) as client:
#     # client.send_message('me', 'Hello, myself!')
#     # print(client.download_profile_photo('me'))
#
#
#     @client.on(events.NewMessage())
#     async def handler(event):
#         if 'Congratulations. Stickers in the set' in event.raw_text:
#             print(event.raw_text)
#             filename = images.pop()
#             await client.send_file(event.chat_id, filename, force_document=True)
#             os.remove(filename)
#
#
#     client.run_until_disconnected()
