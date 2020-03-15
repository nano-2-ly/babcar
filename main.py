import io
import os
import re


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
def is_integer(content):
    try : 
        int(content)
        return True
    except :
        return False

def search_price(candidate):
    for i in candidate:
        for j in candidate:
            for k in candidate:
                if i+j == k:
                    if i>j:
                        return [i,j,k]
                    else:
                        return [j,i,k]

def search_card_number(i):
    
    if '-' in i:
        if '*' in i:
            j = i.replace('*','')
            j = j.replace('-','')

            try : 
                int(j)
                return i
            
            except:
                return False

    return False

def search_date(candidate):
    regex = re.compile(r'^\d{2}/\d{2}/\d{2}')
    matchobj = regex.search(candidate)
    
    if matchobj ==[]:
        return False
    else :
        try :
            return matchobj.group(0)
        except:
            return False

def detect_text(path):
        """Detects text in the file."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        price_candidate = []
        card_number_candidate = []
        date_candidate = []

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            content = text.description
            content = content.replace(',','')
            print('\n"{}"'.format(content))
            
            if is_integer(content):
                price_candidate.append(int(content))
                
            if search_card_number(content):
                card_number_candidate.append(content)

            if search_date(content):
                date_candidate.append(content)

    
        print(search_price(price_candidate))
        print(card_number_candidate)
        print(date_candidate)
    



        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
def detect_document(path):
        """Detects document features in an image."""
        from google.cloud import vision
        import io
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                print('\nBlock confidence: {}\n'.format(block.confidence))

                for paragraph in block.paragraphs:
                    print('Paragraph confidence: {}'.format(
                        paragraph.confidence))

                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        print('Word text: {} (confidence: {})'.format(
                            word_text, word.confidence))

                        for symbol in word.symbols:
                            print('\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('./resources/test.jpg')
detect_text(file_name)