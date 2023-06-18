from multiprocessing import Pool, cpu_count
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import os

def pdf_to_png(pdf_path):
    """
    Converts PDf to PNG images
    """
    output_dir = 'Converted_Images'
    png_files = []
    if not os.path.exists(output_dir) and not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i + 1}.png')
        image.save(image_path, 'PNG')
        png_files.append(image_path)
        print(f'Saved {image_path}')
    return png_files


def dump_tsv(cors_list, text_list, confidence_list, file_name):
    with open(f'{file_name}.tsv', 'w') as file:
        file.write("p1\tp2\tp3\tp4\ttext\tconfidence\n")
        for i in range(len(cors_list)):
            p1, p2, p3, p4 = cors_list[i]
            text = text_list[i]
            confidence = confidence_list[i]
            file.write(f"{p1}\t{p2}\t{p3}\t{p4}\t{text}\t{confidence}\n")

def dump_tsv_from_paddle_res(file_name, res_from_paddle):
    """
    uses paddles result to dump it into a tsv
    """
    cors_list = []
    text_list = []
    confidence_list = []
    for i in range(len(res_from_paddle[0])):
        cors = res_from_paddle[0][i][0]
        cors_list_str = []
        for x in cors:
            my_string = ', '.join(str(element) for element in x)
            cors_list_str.append(my_string)

        text = res_from_paddle[0][i][1][0]
        confidence = res_from_paddle[0][i][1][1]
        cors_list.append(cors_list_str)
        text_list.append(text)
        confidence_list.append(confidence)

    dump_tsv(cors_list, text_list, confidence_list, file_name)


def paddle_inference(im_path):
    ocr_obj = PaddleOCR(use_angle_cls=True, lang='en',det_algorithm="DB",rec_algorithm="SVTR_LCNet")
    file_name = im_path.split("/")[-1].split(".")[0]
    result = ocr_obj.ocr(im_path)
    dump_tsv_from_paddle_res(file_name, result)
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



if __name__ == "__main__":
    im_arr = pdf_to_png("TestOCR.pdf")
    for image in im_arr:
        result = paddle_inference(image)
        ext_text = extract_text(result)
        print(ext_test)