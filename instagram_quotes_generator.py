"""This is a simple script used to scrape a random quote from internet and Create An Instagram Format Post For The Same."""

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm            #Matplotlib Font Manager
from instapy_cli import client                  #Instagram upload interface

def generate_pic(text_color=(225, 225, 225), background_color=(0, 0, 0)):
    """This function takes the quote and creates an image for the same
    It uses standard instagram size and can take an colour background.
    It can also take colour for text also. """
    
    # (612,612) is used for instagram format size.
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
    print(fresh_sentence)
    
    dim = draw_image.textsize(fresh_sentence, font=selected_font)
    x_2 = dim[0]
    y_2 = dim[1]
    draw_image.text(((612/2 - x_2/2), (612/2-y_2/2)), fresh_sentence, align="center",
                    font=selected_font, fill=text_color)
    img.save("quote.png")
    img.show()

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
    # tags_soup = soup.find_all("a", attrs={"class":"tag"})
    # tags_list = [x.text for x in tags_soup]
    
    data = [quote_text, author]
    return data

QUOTE = (" ~ ").join(scrape_quote())
generate_pic()

post_img('hakovut','1qaz2wsx','First Pic #Test')
