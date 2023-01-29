from pdf2image import convert_from_path

SAMPLE1 = r"industrySample/drw2s.pdf"


def convertPDF2JPG(filepath, savename=""):

    images = convert_from_path(filepath)

    for i in range(len(images)):

        # Save pages as images in the pdf
        images[i].save("industrySample/" + savename + str(i) + ".jpg", "JPEG")


convertPDF2JPG(SAMPLE1, "drw2s")
