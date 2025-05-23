# ⚠️ This repo is incomplete, Please check [Our Thesis](https://github.com/AHR-OCR2024/Arabic-Handwriting-Recognition/blob/main/AHR-Thesis.pdf) for more info.

<p align="center">
     <img src="https://github.com/AHR-OCR2024/Arabic-Handwriting-Recognition/assets/169726054/4bcbec06-9ac7-44a8-ad9c-dc3a7c6e13f4" alt="Digital-Ḍād" width="500"/>
   </p>

# Arabic Handwriting Recognition 🖋️

Welcome to the Arabic Handwriting Recognition project! This repository consolidates all the code and data used in our endeavor to create an effective OCR (Optical Character Recognition) system for Arabic script.

This project is proudly made by:

|      Names         |                    |
|--------------------|--------------------|
| Ahmed Taha         | Ayman Saber        |
| Ahmed Nagah        | Abanoub Aied       |
| Kerollos Samir     | Mohamed Abdelfattah|
| Mohamed Fathi      | Nada Asran         |
| Nada Mahmoud       | Rawan Gamal        |
| Reem Fouad         |                    |

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Preprocessing](#preprocessing)
- [AI Training](#aitraining)
- [Full System Diagram](#fullsystemdiagram)
- [Digital-Ḍād ض-الرقمية](#digital-Ḍād)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
Arabic Handwriting Recognition is a project aimed at developing a robust system to accurately recognize and digitize Arabic handwritten text. This repository groups together all the scripts, models, and datasets used throughout the development process.

## Features
- **High Accuracy**: Utilizing advanced machine learning algorithms to ensure high recognition accuracy.
- **Customizable Models**: Easy to retrain and fine-tune models on new datasets.
- **User-Friendly Interface**: Simple interface for testing and utilizing the OCR system.
- **Extensive Dataset**: Includes a comprehensive dataset of Arabic handwritten text.

## Installation
To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/AHR-OCR2024/Arabic-Handwriting-Recognition.git
cd Arabic-Handwriting-Recognition/Application
pip install -r requirements.txt
npm i
```

Download the pretrained models from [here](https://mega.nz/file/0NZlkYAY#lFYQzTWaotIOJ7tYZ5ufPLLbVUP1B5hydpL3y9aPik0) , Put them in Application/Backend/Models

## Usage
To use the OCR system, follow these steps:
1. **Prepare the data**: Ensure your data is in the correct format.
2. **Train the model**: Use the provided training scripts to train the OCR model.
3. **Evaluate**: Test the model on a validation set to check its accuracy.
4. **Run predictions**: Use the trained model to recognize text from new handwritten samples.

To Run the application, run each of these commands in a separate terminial

```bash
python ./Backend/Backend.py
npm run dev
```

## Data
The dataset used in this project is included in the repository. It contains a variety of Arabic handwritten samples to train and evaluate the model. To use the dataset:
1. Download the `Data.rar` file.
2. Extract the contents to the appropriate directory.

## Preprocessing
Preprocessing is a critical stage in the development of our Arabic handwriting recognition system. The goal is to enhance the quality of the input data to ensure accurate recognition. Here are the main steps involved in our preprocessing pipeline:

1. **Image Acquisition**: We collect images of handwritten Arabic text from various sources, including scanned documents and photos taken by digital cameras.
   <p align="center">
     <img src="https://github.com/user-attachments/assets/4a9c7f02-2ae9-46b1-965b-0dbb305202ce" alt="Acquired Image" width="400"/>
   </p>

2. **Geometric Correction**: We correct distortions and warping in the images. Techniques like Hough Line Transform and DocTr (Document Image Transformer) are used to straighten the text lines.

3. **Noise Removal**: We apply filters to remove noise and enhance the clarity of the text. This includes techniques like Gaussian blur and median filtering.
   <p align="center">
     <img src="https://github.com/user-attachments/assets/5ff48966-40f4-498b-8923-cc5a144482c6" alt="Noise Removal" width="400"/>
     <br>
     <em>Unwarped and filtered image</em>
   </p>
   

5. **Segmentation**: We segment the images into paragraphs, lines, and individual characters. This involves methods like histogram projection and CRAFT (Character Region Awareness for Text Detection).
   <p align="center">
     <img src="https://github.com/user-attachments/assets/667f307b-6df3-452e-92f8-c23e66cf040f" alt="image" width="400"/>
   <br>
     <em>Segmented text using CRAFT</em>
   </p>

7. **Normalization**: We normalize the images to a fixed size (64x64) and rescale the pixel values to the range [0, 1] by dividing by 255.0.
   <p align="center">
     <img src="https://github.com/user-attachments/assets/1e22848e-7ee9-4b76-abee-00d69695c854" alt="Final Results" width="400"/>
   <br>
     <em>Final Results</em>
   </p>
   
## AI Training

The AI training phase involves developing and training deep learning models to recognize and digitize handwritten Arabic text. Here are the key components of our AI training process:

1. **Prototype Model Experimentation**
We experimented with three different architectures on a small portion of the data (15,477 Samples) at first to identify the most effective model for our Arabic handwriting recognition system. The comparison of the results is shown in the table below:

| Architecture   | CER  | Accuracy |
|----------------|------|----------|
| EfficientNet-B1| 7.3% | 92.7%    |
| VGG19          | 5.4% | 94.6%    |
| ResNet152      | 2.96%| 97.04%   |

<p align="center">
  <img src="https://github.com/user-attachments/assets/9bf2af20-2e08-446f-8042-abe3f27e161e" alt="ResNet152" width="400"/>
   <br>
     <em>ResNet152 Performance Throughout the Epochs</em>
</p>

2. **Dataset Preparation**
We use a combination of the Arabic Alphabet Character dataset and the KHATT dataset. The combined final dataset includes 108,619 samples.

3. **Data Augmentation**
To improve the robustness of our model, we apply various data augmentation techniques, such as rotation, translation, and scaling.

4. **Model Architecture**
We utilize the ResNet50V2 model, pre-trained on the Arabic Alphabet Character dataset. We then continue training on the KHATT dataset using advanced techniques.

<p align="center">
  <img src="https://github.com/user-attachments/assets/778f4236-8eb4-422d-9dc7-df789b6ce9ef" alt="ResNet50V2Alphabet" width="400"/>
   <br>
     <em>ResNet50V2 Performance on Alphabet Dataset</em>
</p>

6. **Training Techniques**
- **Optimizer**: We use the Adam optimizer with specific parameters for efficient training.
- **Learning Rate Scheduler**: A cosine learning rate scheduler is employed to adjust the learning rate dynamically during training.
- **Training Duration**: The model is trained across 70 epochs to ensure convergence and optimal performance.

6. **Evaluation Metrics**
We use Character Error Rate (CER) and accuracy as our primary evaluation metrics. Our final model achieved a CER of 3% and an accuracy of 97% on the test set.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c55f5318-3e1b-49ec-9fa8-d33ecaf92781" alt="ResNet50V2" width="400"/>
   <br>
     <em>ResNet50V2 (Pre-Trained on Alphabet) Performance Throughout the Epochs</em>
</p>

## Full System Diagram

<p align="center">
  <img src="https://github.com/user-attachments/assets/95e18c1f-969d-48c5-a584-85e50b45d467" alt="Diagram" width="400"/>
   <br>
     <em>The Flow of Our System</em>
</p>

## Digital-Ḍād ض-الرقمية
Our application provides a variety of services and models:
<p align="center">
  <img src="https://github.com/user-attachments/assets/5cbaed0c-9a78-4f2e-b6d7-f262328bf529" alt="MainPage" width="600"/>
   <br>
     <em>Main Page of Our Application</em>
</p>

1. **Handwriting OCR**: Utilizing our model simply taking an image of a paragraph written by handwriting, preprocessing the paragraph, and finally performing ocr on the resulting segmented words or sub-words

<p align="center">
  <img src="https://github.com/user-attachments/assets/557d9d83-c279-46c4-822f-666b5919275b" alt="OCRModel" width="600"/>
   <br>
     <em>Handwriting OCR Model</em>
</p>

2. **Exam Grading**: We pass questiong with their specific answers to the model, and utilizing our OCR methodology alongside a LLM with api, we scan the answers written by a student giving it a grade.

<p align="center">
  <img src="https://github.com/user-attachments/assets/de932111-2937-423b-9a42-c696a2706d58" alt="ExamGrader" width="600"/>
   <br>
     <em>Exam Grader Model</em>
</p>

3. **Document Scanner**: Simply scanning an image of a document written by handwriting, performing OCR on it and then assembling the resulting text using a LLM, creating a full digitized version of the document.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
We would like to thank all contributors and the community for their support and feedback. Special thanks to the authors of the datasets and tools used in this project.

Feel free to reach out with any questions or feedback. Let's make Arabic handwriting recognition more accessible and accurate together!

🌟 Happy Coding! 🌟
