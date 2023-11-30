
from PIL import Image, ImageEnhance


def brigthen_image(img_path, factor):
    """Brightens up the image by the certain factor

       Args:
           img_path (string): Path to the target image
           factor (float): Factor to brighten up the image (1 is default; 1.25 is 25%)
       """
    im = Image.open(
        img_path).convert("RGB")

    enhancer = ImageEnhance.Brightness(im)

    enhancer.enhance(factor).save(
        img_path.split(".")[0] + "_enhanced.png"
    )


if __name__ == "__main__":
    img_path = "data/persistent/weekly_uploads/diagon_alley_3/thumbnail.png"
    brigthen_image(img_path, 1.25)
