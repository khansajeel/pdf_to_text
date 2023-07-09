from multiprocessing import Pool, cpu_count
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import sys
import os

def pdf_to_png(pdf_path):
    """
    Converts PDf to PNG images
    """
    output_dir = 'Converted_Images'
    png_files = []
    if not os.path.exists(output_dir) and not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # add poppler path in func arg if necessary. poppler_path=r'C:\Users\Dev Singh\poppler-23.05.0\Library\bin'
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        png_files.append(image_path)
        print(f'Saved {image_path}')
    return png_files



def paddle_inference(im_path):
    ocr_obj = PaddleOCR(use_angle_cls=True, lang='en',det_algorithm="DB",rec_algorithm="SVTR_LCNet")
    result = ocr_obj.ocr(im_path)
    return result

def extract_text(data):
    text_list = []
    for item in data:
        if isinstance(item, list):
            text_list.extend(extract_text(item))
        elif isinstance(item, tuple):
            text = item[0]
            text_list.append(text)
    return text_list

def is_pdf_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == ".pdf"

def is_png_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == ".png"

def dump_result_to_file(content, file_path):
    with open(file_path, "w") as file:
        for item in content:
            file.write(str(item) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide both the input file directory and the output directory.")
        exit

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    im_arr = []
    result = []
    if (is_pdf_file(input_file)):
        im_arr = pdf_to_png(input_file)
    elif(is_png_file(input_file)):
        im_arr.append(input_file)
    else:
        print("This extension type is currently not supported.")
    for i, image in enumerate(im_arr):
        result = paddle_inference(image)
        ext_text = extract_text(result)
        out_path = os.path.join(output_dir, f'result_{i + 1}.txt')
        dump_result_to_file(ext_text, out_path)
        result.append(ext_text)