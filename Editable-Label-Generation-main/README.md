# Editable-Label-Generation

## Table of Contents
- [Project Description](#project-description)
- [Files Description](#files-description)
- [Process Workflow](#process-workflow)
- [Model Explanation](#model-explanation)
- [Feed Information to API and ZPL Code Generation](#feed-information-to-api-and-zpl-code-generation)
- [Contributors](#contributors)


## Project Description
The primary problem this project aims to solve is the inefficiency and complexity involved in the manual creation and modification of labels for Zebra printers. To address this, the project will develop an advanced automated system that leverages Generative AI to convert images of printer labels into Zebra Printer Language (ZPL). 

## Files Description
- API.ipynb: This file includes code for prompt engineering and experiments with the Anthropic API and OpenAI API to generate ZPL code.
- pytesseract.ipynb: This file demonstrates (with graphic example) how the PyTesseract works, along with image preprocessing (by opencv).
- core_pytesseract.ipynb: This file processes each image over the test folder, providing text recognition by PyTesseract.
- compare.ipynb: This file compares the text recogniztion output with the ground truth, providing groundtruth-base metrics: character accuracy and word accuracy.
- TrOCR.ipynb: This file showcases how the TrOCR works.
- EASTOCR.ipynb: This files demonstrates the EAST + TrOCR pipeline. This approach can be further fine-tuned by feeding specific data along with ground truth.
- YOLO.ipynb: This file shows the baseline YOLO model using the training data with differnent loss functions in order to train our model with the bounding box data we manually created.
- YOLOw_Augmented.ipynb: This file further enhances the YOLO model using data augmentation that we beformed using the albumentations package. This model is our best performing model.

## Process Workflow
![Editable_Label_Workflow](https://github.com/user-attachments/assets/7136da11-c04b-44af-914d-51e3aae075a6)

---

## Model Explanation
### Image Detection using YOLO

Objective: YOLO is central to automating object detection for ZPL label generation. It is trained to classify and locate elements such as text, barcodes, and figures, providing bounding box coordinates for further processing. 

#### Key Implementation Details:
Data Preparation: The dataset consisted of 1494 images, with a subset of 400 images split into training, validation, and test sets. Classes included text, barcodes, and figures.  
Bounding Box Annotation: Using the LabelImg tool, bounding boxes were created in the YOLO format ([class_id, x_center, y_center, width, height]).   
Data Augmentation: Techniques like flipping, brightness/contrast adjustments, and rotation were employed to address class imbalance and improve generalization.   

#### Model Training:
Baseline YOLO Model: A pretrained YOLOv5s model was used as a starting point.   
Enhanced Training: Variants of the YOLO model were trained with modifications such as Focal Loss to address class imbalance and data augmentation for improved performance.   
Performance:   
The model achieved its highest accuracy with barcodes but struggled with figures/lines due to class imbalance and complex structures.   
Augmented datasets improved text and figure detection, enabling more accurate bounding box predictions.   

Integration in Workflow:   
YOLO's output (bounding boxes) was utilized for subsequent stages:   
Barcode Recognition (Pyzbar): Decodes barcode regions and determines type, position, and size.   
These outputs were passed to an API for ZPL code generation.   

#### Challenges: 
Imbalanced classes led to lower detection accuracy for figures. 
Some barcodes were too small for the model to interpret effectively. 
Bounding boxes needed validation to ensure accuracy post-augmentation. 

#### YOLO model Outcome:  
Despite limitations, YOLO provided valuable bounding box predictions, which formed the foundation for downstream OCR, barcode recognition, and ZPL generation, ultimately enabling the automated pipeline to achieve its objectives.

---

### OCR Process in the Workflow

The OCR (Optical Character Recognition) component is responsible for extracting textual content from printer label images. It is a critical step in the pipeline, ensuring that all text elements are accurately recognized and passed downstream for ZPL code generation.

#### **1. Role of OCR in the Workflow**
- The OCR module takes input from the **Object Detection** stage, where bounding boxes for text regions are provided.
- Using these bounding boxes, the OCR module focuses specifically on the text regions, ignoring irrelevant elements like barcodes or figures.
- The recognized text is then passed to the API for ZPL code generation.

#### **2. OCR Model: PyTesseract**
- **Model Description**:
  - PyTesseract is a Python wrapper for Google’s Tesseract-OCR engine.
  - It is a lightweight and efficient OCR solution, capable of handling multiple fonts and text sizes.
  - PyTesseract allows fine-tuning via configuration options, enabling adjustments for complex layouts like those found on label images.

- **Why PyTesseract?**
  - **Flexibility**: Supports various configurations, such as page segmentation modes (`--psm`) and OCR engine modes (`--oem`), to optimize for different text scenarios.
  - **Efficiency**: Processes text regions quickly, making it ideal for large-scale batch processing of labels.
  - **Preprocessing Compatibility**: Works well with preprocessed images (e.g., barcodes masked or white-out regions applied).

#### **3. OCR Process Workflow**
The OCR module follows these steps:

1. **Input from Object Detection**:
   - Receives bounding boxes for potential text regions from the Object Detection model (YOLO).

2. **Preprocessing**:
   - Applies image enhancement techniques (if necessary), such as:
     - **Contrast adjustment** for clearer text visibility.
     - **Barcode masking** to remove interference from non-text elements.

3. **Text Recognition**:
   - Extracts text from each bounding box region using PyTesseract.
   - Uses specific configurations to handle multi-region and multi-font text effectively:
     - **`--psm` (Page Segmentation Mode)**: Optimized to recognize sparse or dense text areas.
     - **`--oem` (OCR Engine Mode)**: Configured to use the most suitable recognition method for the dataset.

4. **Output Generation**:
   - Compiles all recognized text into a structured format and passes it to the API for ZPL code generation.
   - Ensures that text from each bounding box is accurately aligned with its position in the original image.

#### **4. Challenges and Solutions**
- **Challenge**: Interference from barcodes and dense text regions.
  - **Solution**: Apply preprocessing techniques like whiting out barcodes or improving bounding box precision.
- **Challenge**: Multi-font and multi-size text.
  - **Solution**: Fine-tune PyTesseract’s configurations to handle varying layouts effectively.
- **Challenge**: OCR accuracy on edge cases (e.g., faint text or overlapping regions).
  - **Solution**: Combine preprocessing (e.g., denoising, thresholding) with advanced bounding box filtering.

#### **5. Future Improvements**
- **Integration with Advanced OCR Models**:
  - Consider retraining transformer-based models like TrOCR for improved recognition of dense or complex layouts.
- **Enhanced Preprocessing**:
  - Automate masking and improve bounding box accuracy to reduce noise in OCR input.

---

### Image Recognition

The **Image Recognition** component is a critical foundation for the entire pipeline, enabling accurate detection of text, barcodes, and figures on labels. This process involves leveraging advanced Convolutional Neural Networks (CNNs) for object detection and classification tasks.

#### **Model Architecture**
The image recognition framework primarily utilizes YOLO (You Only Look Once) models for real-time object detection and classification, optimized with additional data preprocessing and augmentation steps.

#### **Key Features**
- **Multiclass Detection**: Identifies and differentiates between textual content, barcodes, and other graphical elements.
- **Pretrained Models**: YOLOv5s was fine-tuned on custom datasets to improve its performance on label-specific tasks.
- **Data Augmentation**: Techniques like rotation, scaling, flipping, and brightness adjustment were employed to enhance robustness and generalization.
- **Bounding Box Annotation**: Images were labeled with bounding boxes using tools like LabelImg to provide precise input for model training.

#### **Pipeline Workflow**
1. **Input Preprocessing**: Images are resized and normalized to ensure compatibility with the YOLO model.
2. **Detection and Classification**: YOLO outputs bounding boxes, class labels, and confidence scores for all detected objects.
3. **Post-Processing**:
   - Non-Maximum Suppression (NMS) is applied to filter overlapping bounding boxes.
   - Outputs are passed downstream for OCR and barcode processing.

#### **Challenges and Optimizations**
- **Class Imbalance**: Enhanced detection accuracy for underrepresented classes using Focal Loss.
- **Small Object Detection**: Customized anchor boxes and data augmentation improved the detection of smaller objects like fine text or tiny barcodes.
- **Complex Layouts**: Advanced preprocessing techniques, including masking and white-out for irrelevant elements, were employed to simplify complex label layouts.

#### **Outcomes**
The image recognition module provided high-confidence bounding box predictions for downstream OCR and ZPL code generation. This integration ensured a seamless and automated pipeline for label creation.

---

## Feed Information to API and ZPL Code Generation
The final phase of this project was to identify and refine the optimal approach for generating ZPL code from label data, including text, bounding boxes, and barcode metadata. Through systematic exploration and prompt engineering, the OpenAI API was selected as the most effective solution for generating structured ZPL outputs. 

To identify the best-performing API for generating ZPL code from label data, initial trials were conducted with two platforms: OpenAI API (gpt-4o) and Anthropic API (claude-3.5-sonnet). The OpenAI API demonstrated strong performance in handling multi-modal inputs, such as bounding boxes, text, and barcode data, and consistently generated relevant and well-structured ZPL outputs. In contrast, the Anthropic API showed limited promise in producing structured ZPL code, often failing to handle the complex metadata effectively. After a thorough comparative analysis, the OpenAI API was selected for its superior ability to integrate diverse data types and deliver accurate and consistent results, making it the optimal choice for this project.

*Baseline Experimentation*

In the baseline approach, a general prompt was used to detect metadata (e.g., text, figures, and barcodes) and generate ZPL code. While the API produced functional outputs, the lack of structured input data, such as bounding box coordinates, resulted in imprecise label formatting. OpenAI API consistently outperformed Anthropic, delivering more structured and relevant outputs, but the results highlighted the need to incorporate spatial context for improved precision.

*Incorporating Bounding Box Information*

To address the lack of spatial context in the baseline approach, bounding box data was introduced to provide precise location information for text and barcodes. This enhancement allowed the API to generate ZPL code with improved accuracy in element alignment and formatting. The initial challenge was that the baseline prompt lacked contextual details about object placement, leading to inconsistencies in the output. By integrating bounding box coordinates into the prompt, the API was able to understand spatial relationships, resulting in significantly enhanced precision and accurate positioning of label elements.

*Adding Text Metadata*

Building on the integration of bounding box data, textual content was added to provide semantic clarity, enabling the API to interpret and align text elements with their respective bounding boxes more effectively. The initial challenge was that the API required explicit textual data to fully understand the label content. To address this, both bounding box and text information were incorporated into the prompt. This enhancement improved the API's comprehension of the label structure, leading to better alignment and a more accurate representation of text elements in the ZPL output.

*Enhancing Prompts with Barcode Data*

Building on the integration of bounding box and text data, barcode information was incorporated into the prompts to provide critical structural and validation data for the API. The barcode metadata, including type and count, was essential for ensuring that the generated ZPL code accurately represented the expected label format. The initial challenge was that the absence of explicit barcode details in the prompts limited the API's ability to validate and generate precise outputs for barcode elements. By including this metadata extracted from the Pyzbar model, the API was able to accurately identify, encode, and position barcodes within the label. This enhancement improved the reliability of the ZPL code generation process by ensuring that the barcodes matched the input expectations in terms of type, count, and placement, thereby reducing errors and improving label accuracy.

*Key Findings and Learnings*

Throughout the project, several critical insights and advancements were made, which significantly enhanced the performance and reliability of the ZPL code generation pipeline. Incremental prompt engineering proved to be a powerful tool, allowing us to systematically refine API outputs and address specific challenges. Integrating bounding box and text metadata into the prompts was a key breakthrough, as it provided spatial and semantic context, enabling the API to produce more accurate and well-structured ZPL code. Furthermore, incorporating barcode information into the workflow not only improved the accuracy of barcode elements but also facilitated output validation by ensuring alignment with the expected label structure. These findings highlight the importance of iterative development and the value of combining multiple data modalities to optimize AI-driven solutions.

## Contributors
- Yumin Zhang
- Inu Tenneti
- Louise Liu
- Darwin Ye
