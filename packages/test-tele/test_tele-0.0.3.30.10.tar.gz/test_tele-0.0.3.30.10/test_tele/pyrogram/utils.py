import json
import shlex
import asyncio
import logging


OFFSET_PID = 50
IMG_EXT = ['jpg', 'webp', 'png', 'heic', 'jpeg']
GIF_EXT = ['gif']
VID_EXT = ['mp4', 'webm']


async def get_tags(tags: list[str], limit: int = 0) -> str:
    real_tags = []
    i = 0
    for tag in tags:
        if limit != 0:
            i += 1
        decoded_str = tag.encode('utf-8').decode('utf-8')
        real_tags.append(f"`{decoded_str}`")
        if limit != 0 and i == limit:
            break
    all_tags = f'{(", ").join(real_tags)}'
    return all_tags


async def gallery_dl(url: str, pid=0, offset=OFFSET_PID, force_kill=None, filter='--range'):
    """Start subprocess gallery-dl"""

    command = shlex.split(f'gallery-dl \"{url}\" --config-ignore -c config/config.json -j {filter} {pid + 1}-{pid + offset}')

    # logging.warning((" ").join(command))
    
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        
        if force_kill:
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=force_kill)
            except asyncio.TimeoutError:
                process.kill()
        else:
            stdout, stderr = await process.communicate()

        if process.returncode != 0:
            if not force_kill:
                raise Exception(f'gallery-dl failed with return code {process.returncode}: {stderr.decode()}')
        else:
            result = json.loads(stdout.decode())
            return result
        
    except Exception as err:
        logging.error(err)


async def turn_into_gif(elemen) -> str:
    if elemen[2]['extension'] == 'webm':
        url = elemen[1]
        gif_url = url[:-5] + ".gif"
        return gif_url
    return elemen[1]

