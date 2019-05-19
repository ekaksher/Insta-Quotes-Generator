"""This is a simple script used to scrape a random quote from internet and Create An Instagram Format Post For The Same."""

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import matplotlib.font_manager as fm            #Matplotlib Font Manager
from instapy_cli import client                  #Instagram upload interface
from json import loads
from io import BytesIO

def generate_pic(tag=None,text_color=(225, 225, 225), background_color=(0, 0, 0)):
    """This function takes the quote and creates an image for the same
    It uses standard instagram size and can take an colour background.
    It can also take colour for text also. """
    
    if tag != None:
        #Try to fetch relevant background. If not found, use default plain background
        try:
            img, flag = background_image(tag), 0
        except:
            flag = 1
    elif tag == None or flag == 1:     
        img = Image.new('RGB', (612, 612), color=background_color)

    draw_image = ImageDraw.Draw(img)
        
    selected_font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='cinzel.otf')),30)
    sum_quote = 0
    
    # this loops gets textsize of every letter in the quotes and adds it.
    for letter in QUOTE:
        sum_quote += draw_image.textsize(letter, font=selected_font)[0]
    average_length_of_letter = sum_quote/len(QUOTE)
    number_of_letters_for_each_line = (612/1.618)/average_length_of_letter
    
    incrementer = 0
    fresh_sentence = ''
    # creates a fresh sentense in proper format.
    for letter in QUOTE:
        if letter == '~':
            fresh_sentence += '\n\n' + letter
        elif incrementer < number_of_letters_for_each_line:
            fresh_sentence += letter
        else:
            if letter == ' ':
                fresh_sentence += '\n'
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer += 1
    
    dim = draw_image.textsize(fresh_sentence, font=selected_font)
    x_2 = dim[0]
    y_2 = dim[1]
    draw_image.text(((612/2 - x_2/2), (612/2-y_2/2)), fresh_sentence, align="center",
                    font=selected_font, fill=text_color)
    img.save("quote.png")

def post_img(uname,pwd,caption="Quote Upload"):
    ''' Uses instapy-cli library (pip install instapy-cli).
        Post image on Instagram on the profile with username 'uname' and password 'pwd' & optional 'caption' '''

    with client(uname,pwd) as cli:
        cli.upload('quote.png',caption)

def scrape_quote():
    """This function scrapes a random quote from internet along with its
     author and tags related to it. """
    
    res = requests.get("http://quotes.toscrape.com/random", timeout=5)
    soup = BeautifulSoup(res.content, "html.parser")
    quote_text = soup.find("span", attrs={"class":"text"}).text
    author = soup.find("small", attrs={"class":"author"}).text
    
    #tags to used later on.
    tags_soup = soup.find_all("a", attrs={"class":"tag"})
    tags_list = [x.text for x in tags_soup]
    
    data = [quote_text, author, tags_list]
    return data

def background_image(query):
    """Fetch a bacground using 'query' and the pixabay.com API interface.
        Converts image into square format and reduces brightness to improve font visibiliy"""

    api_url = "https://pixabay.com/api/?key=12526365-dfdf19580d00e2bec566327fc&q="+query.replace(' ','+')+"&image_type=photo"
    resp = requests.get(api_url)
    jresp = loads(resp.text)
    img_link = jresp['hits'][0]['largeImageURL']
    response = requests.get(str(img_link))
    img = Image.open(BytesIO(response.content))
    cropped = img.crop((0,0,612,612))
    enh = ImageEnhance.Brightness(cropped)
    cropped = enh.enhance(0.3)
    
    return cropped

scrape_results = scrape_quote()

QUOTE = (" ~ ").join(scrape_results[:2])
generate_pic(scrape_results[-1][0])

#Generate a string of all tags as hashtags to be used as caption
tag_string = ['#'+tag for tag in scrape_results[-1]]
tag_caption = ' '.join(tag_string)

#Post Image on the account username=1st argument, password=2nd argument
post_img('botquotes.py','1qaz2wsx',tag_caption) #CHANGE USERNAME & PASSWORD TO POST TO PROFILE OF CHOICE
