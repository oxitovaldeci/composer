import io
from PIL import Image


def cprint(*args, **kwargs):
    style = "\033[" + str(kwargs.pop("style", "31")) + "m"
    a_list = []
    for obj in args:
        a_list.append(style + str(obj) + "\033[0m")
    args = a_list
    print(*args, **kwargs)


def squarify(file):
    """
    Retorna imagem no formato quadrado e
    reduz sua resolução se necessário.
    """
    image = Image.open(file)

    image = image.convert("RGB")

    width, height = image.size
    max_length = 2000

    if height != width:
        top = 0
        left = (width - height) / 2
        right = (width + height) / 2
        bottom = height
        if width < height:
            left = 0
            right = width
            bottom = width
        image = image.crop((left, top, right, bottom))

    if width > max_length and height > max_length:
        image.thumbnail((max_length, max_length))

    output = io.BytesIO()
    image.save(output, format="JPEG")
    output.seek(0)
    return output
