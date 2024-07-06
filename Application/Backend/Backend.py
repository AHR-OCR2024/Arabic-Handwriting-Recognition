import warnings
warnings.filterwarnings("ignore")
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io, os, subprocess
import base64
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import asyncio

import cv2
import numpy as np
from skimage.color import rgb2gray
from PIL import Image
import tensorflow as tf
from skimage.filters import threshold_otsu
import keras_ocr
import keras
from keras.models import load_model
from keras.layers import StringLookup


# limit gpu vram usage to 4GB
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(
                gpus[0],
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*4)])  # Limit to 4GB
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)

model_path = 'Backend/Models/Res50V2Alpha_without_CTC.h5'
predictor = load_model(model_path)
print("Model", model_path,"Loaded")
AUTOTUNE = tf.data.AUTOTUNE

## Edit 1: Made sure the directories exist or made of they don't
def check_dir_remove_files(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
        files = os.listdir(path)
        if len(files) != 0:
            # delete all files in the directory
            for f in files:
                os.remove(os.path.join(path, f))

def inser_img(image, distorted_path, img_name):
    cv2.imwrite(distorted_path + img_name, image)
    print("Copied the image to", distorted_path)
    
def run_inference_doctr(geometric_unwrapping, illumination_rectifying):
    # Define the base directory and script path
    base_dir = os.path.abspath("Backend/DocTr")
    script_path = "inference.py"  # script path relative to base_dir
    
    # Define the command to run the script
    if geometric_unwrapping and not illumination_rectifying:
        command = ["python", script_path]
    elif illumination_rectifying and not geometric_unwrapping:
        command = ["python", script_path, "--ill_rec", "True", "--disable_geo"]
    elif illumination_rectifying and geometric_unwrapping:
        command = ["python", script_path, "--ill_rec", "True"]
    print("Command to send: ", command)
    
    # Run the command from the base_dir
    result = subprocess.run(command, capture_output=True, text=True, cwd=base_dir)
    
    print("Finished Running DocTr Inference")
    
    return result

def check_dir_copy_file(paths):
    for path in paths:
        files = os.listdir(path)
        if len(files) != 0:
            img = cv2.imread(path + files[0])
            cv2.imwrite('Backend/Image_Store/uploaded_image.jpg', img)
            break
    print("Finished Copying File Back")

def denoise(img):
    image_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    dst = cv2.fastNlMeansDenoising(image_gray, h=25, templateWindowSize=15, searchWindowSize=35)
    return dst

def resize(img, max_dim=2000):
    if isinstance(img, Image.Image):
        width, height = img.size
        if width > max_dim or height > max_dim:
            if width > height:
                ratio = max_dim / width
            else:
                ratio = max_dim / height
            img = img.resize((int(width * ratio), int(height * ratio)), Image.LANCZOS)
    elif isinstance(img, np.ndarray):
        height, width = img.shape[:2]
        if width > max_dim or height > max_dim:
            if width > height:
                ratio = max_dim / width
            else:
                ratio = max_dim / height
            img = cv2.resize(img, (int(width * ratio), int(height * ratio)), interpolation=cv2.INTER_LANCZOS4)
    return img

def preproces_image(image, *, kernel_size=15, crop_side=50, blocksize=35, constant=15, max_value=255):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bit = cv2.bitwise_not(gray)
    image_adapted = cv2.adaptiveThreshold(
        src=bit,
        maxValue=max_value,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=blocksize,
        C=constant,
    )
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    erosion = cv2.erode(image_adapted, kernel, iterations=2)
    return erosion[crop_side:-crop_side, crop_side:-crop_side]

# def find_edges(image_preprocessed, *, bw_threshold=150, limits=(0.2, 0.15)):


# def adapt_edges(edges, *, height, width):


#image contrast enhancement
def grayscalize(img):
    #check if its 3 channel or grayscale, based on that convert to grayscale
    if img.ndim > 2: # is this is a rgb/rgba image
        img = rgb2gray(img)
    return img

def binarize_image(image):
    threshold = threshold_otsu(image)
    return image < threshold


def denoise_binary_image(binary_image, kernel_size=5):
    # Define a kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    # Perform erosion followed by dilation to remove noise
    denoised_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    return denoised_image

def thresholding(image, threshold, typee='Binary', param1=0, param2=0):
    if(typee.lower()=='binary'):
        ret, thresh= cv2.threshold(image,threshold,255,cv2.THRESH_BINARY_INV)
    else:
        thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,param1,param2)
    return thresh

def edg_enhance(image):
    gray = grayscalize(image)
    binarized_image = binarize_image(gray)
    binarized_image_uint8 = (binarized_image * 255).astype(np.uint8)
    
    return binarized_image_uint8

# def PreProcessTheImage(image):


def DetectWords(image):
    # padding_size = 100
    # image = np.pad(image, ((padding_size, padding_size), (padding_size, padding_size), (0, 0)), mode='constant', constant_values=255) #broken
    words_array = []
    try:
        
        ## Edit 3: Tuned the keras ocr model for better results
        ## text thresh: 0.2 --> 0.3, link thresh: 0.6 --> 0.7, size thresh: same, margin: 10 --> 0, thickness: 0.4 --> 0.2 (BOXES JUST FOR SHOW DOESN'T AFFECT RESULTS)
        
        detector = keras_ocr.detection.Detector(weights='clovaai_general')
        boxes = detector.detect(images=[image], text_threshold=0.3, link_threshold=0.7, size_threshold=10)[0]
        for _, box in enumerate(boxes):
            cropped_img = keras_ocr.tools.warpBox(image=image, box=box, margin=0)
            words_array.append(cropped_img)
        image_with_boxes = keras_ocr.tools.drawBoxes(image=image, boxes=boxes, color=(0, 0, 255), thickness=1, boxes_format='boxes')
    except:
        print('error')
        image_with_boxes = image  # Return the original image if there's an error
    return words_array, image_with_boxes

## Edit 5: Clean edges function -> Used for dealing with overcutting or leftovers in segmented images whether vertically y (up or down), or horizontally (left, right),
# padding of each and thresholding is adjusted according to need

def clean_edges(image, x_padding=4, y_padding=15):
    # Ensure the image is in grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Convert to binary image with a lower threshold value
    _, binary = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY_INV)  # Adjust the threshold value as needed
    
    # Optional: Use dilation to make the words thicker
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If no contours are found, return the original image
    if not contours:
        return image
    
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Add padding around the bounding box
    x = max(0, x - x_padding)
    y = max(0, y - y_padding)
    w = min(image.shape[1] - x, w + 2 * x_padding)
    h = min(image.shape[0] - y, h + 2 * y_padding)
    
    # Crop the image to the bounding box with padding
    cleaned_image = image[y:y+h, x:x+w]
    
    return cleaned_image



def cropLineToWords(viable_sequences, image):
    (w,h) = image.shape
    words = [image[0:w-1, viable_sequences[i-1]:viable_sequences[i]] for i in range(1,len(viable_sequences))]
    words.append(image[0:w-1, viable_sequences[-1]:h-1])
    return words

def removeSpaces(words):
    return [word for word in words if np.sum(word[:,:]>0)]

def directionalHistogram(img, direction='H'):
    (w,h) = img.shape
    pixel_count = 0
    if(direction=='H'):
        return [img[j].tolist().count(255) for j in range(w-1)]
    else:
        return [img[:,j].tolist().count(255) for j in range(h-1)]

def IslandSegmentation(words_array):
    segmented_words = []
    for image in words_array:
        words = []
        (w,h) = image.shape
        hist_vertical = directionalHistogram(image, direction='V')
        zero_sites = np.where(np.asarray(hist_vertical)==0)[0]
        sequences = [[zero_sites[i-1], zero_sites[i]] for i in range(1, len(zero_sites)) if zero_sites[i] != zero_sites[i-1] + 1]
        if not sequences:
            continue
        sequence_lengths = [seq[1] - seq[0] + 1 for seq in sequences]
        average_sequence_length = sum(sequence_lengths[1:-1]) / len(sequences)
        overlap_factor = 0.75 * average_sequence_length
        viable_sequences_unrolled = [seq[0] for seq in sequences if seq[1] - seq[0] + 1 >= average_sequence_length - overlap_factor] + [-1]
        if viable_sequences_unrolled[0] != 0:
            viable_sequences_unrolled = [0] + viable_sequences_unrolled
        words.append(cropLineToWords(viable_sequences_unrolled, image))
        ordered_words = [word if np.sum(word[:,:]) else 'space' for word in words[0]]
        for ordered_word in ordered_words:
            if not isinstance(ordered_word, str):
                segmented_words.append(ordered_word)
    
    return segmented_words
    
def clean_segment(image):
    clean_value = 0.065 #TODO: Tune this value
    # get max value in the image
    max_value = np.max(image)
    # normalize the image to range [0, 1]
    normalized_image = image / max_value
    # get average brightness of the image
    avg = np.average(normalized_image)
    # if the image is too small or too dark, return 'space'
    if image.shape[1] < 10 and avg < 0.05:
        return 'space'
    elif avg <= clean_value:
        return 'space'
    elif avg > clean_value:
        return image
    return image

def crop_image(image, direction='H'):
    w,h=image.shape
    if(w<10 or h<10):
        return image
    hist=directionalHistogram(image, direction )
    flipped_hist=np.flip(hist)
    try:
        startpos = next(i for i in range(1, len(hist)-1) if hist[i-1]==0 and hist[i]==0 and hist[i+1]!=0)
        endpos = len(flipped_hist)-1 - next(i for i in range(1, len(flipped_hist)-1) if flipped_hist[i-1]==0 and flipped_hist[i]==0 and flipped_hist[i+1]!=0)
    except StopIteration:
        return image
    cropped_image = image[startpos:endpos,:] if direction == 'H' else image[:,startpos:endpos]
    if cropped_image.shape[0] <= 0 or cropped_image.shape[1] <= 0:
        return image
    return cropped_image

def distortion_free_resize(image, img_size=(64, 64)):
    h,w= img_size
    if h <= 0 or w <= 0:
        raise ValueError("Image size must be positive")
    if image.shape[0] <= 0 or image.shape[1] <= 0:
        return image
    # convert to 3-channel image
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = tf.image.resize(image, size=(h, w), preserve_aspect_ratio=True)
    pad_height = h - tf.shape(image)[0]
    pad_width = w - tf.shape(image)[1]
    pad_height_top = pad_height // 2 if pad_height % 2 == 0 else pad_height // 2 + 1
    pad_width_left = pad_width // 2 if pad_width % 2 == 0 else pad_width // 2 + 1
    image = tf.pad(image, paddings=[[pad_height_top, pad_height//2], [pad_width_left, pad_width//2], [0, 0]])
    image = tf.transpose(image, perm=[1, 0, 2])
    image = tf.image.flip_left_right(image)
    return image

def perform_padding(image):
    image_v_cropped=crop_image(image, 'V')
    image=distortion_free_resize(image_v_cropped)
    image=np.rot90(image)
    return image

def PrepareCharacters():
    characters = {'ء','آ','أ','ؤ','إ','ئ','ا','ب','ة','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك','ل','م','ن','ه','و','ى','ي'}
    max_len = 7
    # Mapping characters to integers.
    char_to_num = StringLookup(vocabulary=sorted(list(characters)), mask_token=None)

    # Mapping integers back to original characters.
    num_to_char = StringLookup(
        vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
    )
    return char_to_num, num_to_char, max_len


def decode_batch_predictions(pred, num_to_char, max_len=7):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search.
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_len
    ]
    # Iterate over the results and get back the text.
    output_text = []
    for res in results:
        res = tf.gather(res, tf.where(tf.math.not_equal(res, -1)))
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text

def perform_DocTr(illumination_rectifying,
                  geometric_unwrapping,
                  distorted_path = 'Backend/DocTr/distorted/',
                  geo_rec_path = 'Backend/DocTr/geo_rec/',
                  ill_rec_path = 'Backend/DocTr/ill_rec/',
                  img_path = 'Backend/Image_Store/uploaded_image.jpg'):
    image = cv2.imread(img_path)
    print("DocTr: Image Read")
    image = resize(image, max_dim=1500)
    print("DocTr: Finished Resizing")
    check_dir_remove_files([distorted_path, geo_rec_path, ill_rec_path])
    print("DocTr: Removed Old Files")
    inser_img(image, distorted_path, 'distorted.jpg')
    print("DocTr: Inserted Image")
    print("DocTr: Running Inference")
    run_inference_doctr(geometric_unwrapping, illumination_rectifying)
    print("DocTr: Finished Inference")
    check_dir_copy_file([ill_rec_path, geo_rec_path, distorted_path])
    print("DocTr: Copied Files")

def encode_images_to_base64(images):
    imgs_arr_base64 = []
    for img in images:
        buffered = io.BytesIO()
        img = Image.fromarray((img * 255).astype(np.uint8))  # convert to uint8
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        imgs_arr_base64.append(img_str)
    return imgs_arr_base64
def model1_process():
    # Read Image
    image = cv2.imread("Backend/Image_Store/uploaded_image.jpg")
    # Preprocessing
    Preprocessedimage = resize(image, max_dim=2000)
    print("Finished Preprocessing")
    WordSegments, image_with_boxes = DetectWords(Preprocessedimage)
    # save image with boxes to disk
    cv2.imwrite("Backend/Image_Store/image_with_boxes.jpg", image_with_boxes) #TODO: return image to front end
    print("Finished Word Segmentation")
    # Enhance Edges
    WordSegments = [edg_enhance(image) for image in WordSegments]
    print("Finished Edge Enhancement")
    # Cleaning Eges
    CleanedWordSegments = [clean_edges(image) for image in WordSegments]
    # Island Segmentation
    IslandSegments = IslandSegmentation(CleanedWordSegments)
    print("Finished Island Segmentation")
    # Clean Segments
    segmented_words = [clean_segment(image) for image in IslandSegments]
    print("Finished Cleaning Segments")
    # remove spaces
    segmented_words_cleaned = [word for word in segmented_words if not isinstance(word, str)]
    print("Finished Removing Spaces")

    # padding
    segmented_words = []
    for image in segmented_words_cleaned:
        try:
            padded_image = perform_padding(image)
            segmented_words.append(padded_image)
        except Exception as e:
            print(f"Error while padding image: {e}")
    print("Finished Padding")
    segmented_words = np.array(segmented_words)
    # scale images
    segmented_words = segmented_words / 255.0
    print("Finished Scaling")
    # prepare characters
    char_to_num, num_to_char, max_len = PrepareCharacters()
    input_array = np.zeros((segmented_words.shape[0],7))
    encoded_predictions = predictor.predict([segmented_words, input_array])
    print("Finished Predicting")
    finalLabels = decode_batch_predictions(encoded_predictions, num_to_char, max_len)
    print("Finished Decoding")
    
    # resize images in segmented_words to at least (170x90)
    resized_images = []
    for img in segmented_words:
        img_pil = Image.fromarray((img * 255).astype(np.uint8))  # convert to uint8
        width, height = img_pil.size
        aspect_ratio = width / height
    
        if width < 170 or height < 90:
            if width < height:
                new_width = 170
                new_height = round(new_width / aspect_ratio)
            else:
                new_height = 90
                new_width = round(new_height * aspect_ratio)
    
            img_pil = img_pil.resize((new_width, new_height), Image.LANCZOS)
        resized_images.append(np.array(img_pil) / 255.0)  # convert back to float
    print("Finished Resizing for view")
    segmented_words = np.array(resized_images)
    # encode images to base64
    imgs_arr_base64 = encode_images_to_base64(segmented_words)
    print("Finished Encoding")
    
    return imgs_arr_base64, finalLabels

def model2_process():
    # send image to OCR
    prompt_script = "Backend/Exam_Grading/OCR.py"
    image_path = "Backend/Image_Store/uploaded_image.jpg"
    ocr_output_path = "Backend/Exam_Grading/ocr.txt"
    # python_path = "M:/Others/Miniconda/python.exe"  # specify the python path
    python_path = 'python'
    command = f"{python_path} {prompt_script} {image_path} {ocr_output_path}"
    print("Command to send:", command)
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running prompt script: {e.stderr.decode('utf-8').strip()}")
    
    # Call the grading script with the recognized text
    grading_script = "Backend/Exam_Grading/Grade.py"
    # python_path = "M:/Others/Miniconda/python.exe"  # specify the python path
    python_path = 'python'
    command = f"{python_path} {grading_script}"
    print("Command to grade:", command)
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Read the grades from the file "grades.txt"
        grades_output_path = "Backend/Exam_Grading/grades.txt"
        try:
            with open(grades_output_path, "r", encoding="utf-8") as f:
                grades_result = f.read()
            print(f"Grades read from {grades_output_path}")
        except Exception as e:
            print(f"Error reading grades: {str(e)}")
            grades_result = None
        
        return grades_result

        # print("Grading Output:", grading_output)
    except subprocess.CalledProcessError as e:
        print(f"Error running grading script: {e.stderr.decode('utf-8').strip()}")

def model3_process():
    rectified_image_path = "Backend/Image_Store/uploaded_image.jpg"

    # Check if the rectified image exists
    if not os.path.exists(rectified_image_path):
        print("Rectified image not found")
        return None

    # Read the rectified image
    rectified_image = cv2.imread(rectified_image_path)
    if rectified_image is None:
        print("Failed to read rectified image")
        return None

    # Encode the image to base64
    with open(rectified_image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()

    return encoded_image

def model4_process():
    # send image to OCR
    prompt_script = "Backend/Exam_Grading/OCR.py"
    image_path = "Backend/Image_Store/uploaded_image.jpg"
    ocr_output_path = "Backend/Exam_Grading/ocr.txt"
    # python_path = "M:/Others/Miniconda/python.exe"  # specify the python path
    python_path = 'python'
    command = f"{python_path} {prompt_script} {image_path} {ocr_output_path}"
    print("Command to send:", command)
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running prompt script: {e.stderr.decode('utf-8').strip()}")
    # Read the OCR text from the file "ocr.txt"
    ocr_output_path = "Backend/Exam_Grading/ocr.txt"
    try:
        with open(ocr_output_path, "r", encoding="utf-8") as f:
            ocr_result = f.read()
        print(f"OCR read from {ocr_output_path}")
    except Exception as e:
        print(f"Error reading OCR: {str(e)}")
        ocr_result = None
    return ocr_result

def process_requsted_image(selected_model, geometric_unwrapping, illumination_rectifying):
    print("main function called")
    if geometric_unwrapping == True or illumination_rectifying == True:
        print("Calling DocTr")
        perform_DocTr(illumination_rectifying, geometric_unwrapping)
        print("Finished Performing DocTr")
        
    if selected_model == 'model1':
        return model1_process()
    elif selected_model == 'model2':
        return model2_process()
    elif selected_model == 'model3':
        return model3_process()
    elif selected_model == 'model4':
        return model4_process()
        

def processing_time(start_time, end_time):
    print(f"Processing time: {end_time - start_time} seconds")
    return end_time - start_time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/upload-image", methods=["POST"])
def upload_image():
    start_time = time.time()
    if "image" not in request.files:
        end_time = time.time()
        processing_time(start_time, end_time)
        return jsonify({"error": "No image file uploaded"}), 400

    # Get request data
    image = request.files["image"] # Get the image file from the request
    selected_model = request.form.get("model", "model1")  # Get Selected Model from the request, Default to "model1" if not provided
    geometric_unwrapping = request.form.get("geometricUnwrapping", "false").lower() == "true" # Get Geometric Unwrapping from the request, Default to "false" if not provided
    illumination_rectifying = request.form.get("illuminationRectifying", "false").lower() == "true" # Get Illumination Rectifying from the request, Default to "false" if not provided
    print("Processing: ", image.filename)
    print("Selected Model: ", selected_model)
    print("Geometric Unwrapping: ", geometric_unwrapping)
    print("Illumination Rectifying: ", illumination_rectifying)

    if selected_model == 'model2':
        exam_a = request.form.get("exam_a") # Get Exam Answer from the request
        try:
            with open("Backend/Exam_Grading/QwAnswers.txt", "w") as answer_file:
                answer_file.write(exam_a)
            print("Exam Question and Answer Written to File")
        except Exception as e:
            end_time = time.time()
            timed = processing_time(start_time, end_time)
            print(f"Error writing exam question and answer to file: {e}")
            return jsonify({"error": "Failed to write exam question and answer to file", "message": f"{e}", "time": timed}), 500

    if not image.filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")): # Check if the image format is valid
        print("Received invalid image format")
        end_time = time.time()
        timed = processing_time(start_time, end_time)
        return jsonify({"error": "Invalid image format","message":"Invalid image format","time": timed}), 400
    
    # else continue with the rest of the code
    try:
        # Read Image
        image_data = image.read() # Read the image data from the request
        print("image read")
        img = Image.open(io.BytesIO(image_data)) # Open the image data as an image object
        #save image to disk
        img = img.convert("RGB") # Convert the image to RGB format
        img.save("Backend/Image_Store/uploaded_image.jpg") # Save the image
        print("image opened")
        
        # Pass the image and selected model to the function
        if selected_model == 'model1':
            imgs_arr, labels_arr = process_requsted_image(selected_model, geometric_unwrapping, illumination_rectifying)
            print("Success: Image Processed Successfully!")
            end_time = time.time()
            timed = processing_time(start_time, end_time)
            return jsonify({"images": imgs_arr, "labels": labels_arr, "time": timed}),200
        elif selected_model == 'model2':
            grades = process_requsted_image(selected_model, geometric_unwrapping, illumination_rectifying)
            if grades != None:
                print("Success: Image Processed Successfully!")
                end_time = time.time()
                timed = processing_time(start_time, end_time)
                return jsonify({"grades": grades, "time": timed}),200
            else:
                timed = processing_time(start_time, end_time)
                return jsonify({"error": "Failed to process image", "message": "Failed to process image", "time": timed}), 500
        elif selected_model == 'model3':
            rectified_image = process_requsted_image(selected_model, geometric_unwrapping, illumination_rectifying)
            if rectified_image != None:
                print("Success: Image Processed Successfully!")
                end_time = time.time()
                timed = processing_time(start_time, end_time)
                return jsonify({"rectified_image": rectified_image, "time": timed}),200
            else:
                end_time = time.time()
                timed = processing_time(start_time, end_time)
                return jsonify({"error": "Failed to process image", "message": "Failed to process image", "time": timed}), 500
        elif selected_model == 'model4':
            ocr_text = process_requsted_image(selected_model, geometric_unwrapping, illumination_rectifying)
            if ocr_text != None:
                print("Success: Image Processed Successfully!")
                end_time = time.time()
                timed = processing_time(start_time, end_time)
                return jsonify({"ocr_text": ocr_text, "time": timed}),200
            else:
                end_time = time.time()
                timed = processing_time(start_time, end_time)
                return jsonify({"error": "Failed to process image", "message": "Failed to process image", "time": timed}), 500
        
    except Exception as e:
        print(f"Error processing image: {e}")
        end_time = time.time()
        timed = processing_time(start_time, end_time)
        return jsonify({"error": "Failed to process image", "message": f"{e}", "time": timed}), 500


if __name__ == '__main__':
    from waitress import serve

    async def start_server():
        serve(app, host='localhost', port=5000)

    async def main():
        print("Server started at http://localhost:5000")
        await start_server()

    if __name__ == '__main__':
        asyncio.run(main())