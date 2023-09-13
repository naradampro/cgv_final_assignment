#import the needed packages
import pytesseract 

def extract_text_from_image(img, lang='eng'):
    
    try:
        # Extract text from the image
        text = pytesseract.image_to_string(img, lang=lang)
        return text
    except Exception as e:
        print("Error:", e)
        return None

#Usage:
 

# # Call the function to extract text
# extracted_text = extract_text_from_image(img)

# if extracted_text is not None:
#     print("Extracted Text:", extracted_text)
# else:
#     print("Text extraction failed.")

