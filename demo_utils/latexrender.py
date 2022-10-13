import base64
import io
from PIL import Image
from matplotlib import mathtext, font_manager
import matplotlib as mpl


def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image"""
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


# https://stackoverflow.com/questions/57316491/how-to-convert-matplotlib-figure-to-pil-image-object-without-saving-image
def latex_to_base64(latex):
    mpl.rcParams["savefig.transparent"] = True

    texFont = font_manager.FontProperties(size=30, family="serif", math_fontfamily="cm")

    buf = io.BytesIO()
    mathtext.math_to_image(f"${latex}$", buf, prop=texFont, dpi=300, format="png")

    buf.seek(0)
    return base64.b64encode(buf.getbuffer())
