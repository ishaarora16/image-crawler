import re
import os
import lxml
import sys
import urllib.request
import urllib3
import requests
import certifi
from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect #render_template = Generating HTML from within Python 



ic = Flask(__name__)

count = 0


@ic.route("/")
def main():
    if count == 1:
        return render_template("index.html", result=str((str(count) + " Image Downloaded !")))
    else:
        return render_template("index.html", result=str((str(count) + " Images Downloaded !")))


@ic.route("/get_images", methods=['POST'])

def get_images():
    _url = request.form['inputURL'] #accpeting the url
    try:
        global count
        count = 0
        code = requests.get(_url, auth=('[username]','[password]'), verify=True)  #its a response object,we can get all the information required from this object
        text = code.text #request guess the encoding of the response ,this code.text is for the request to use the encoding of response .encoding : utf -8
        soup = BeautifulSoup(text,"lxml")  #accepts a string or a opened text file
        for img in soup.findAll('img'): #takes out all the img tag
            count += 1
            if (img.get('src'))[0:4] == 'http':
                src = img.get('src')
            elif(img.get('src'))[0:5] == 'https':
                src = img.get('src')
            else:
                src = urljoin(_url, img.get('src')) #if the url starts from /dquw/wf to add the domain name to the incomplete url.
            download_image(src)  #passing the url of the image
        return redirect("http://localhost:5000")  #if every thing works fine we are directed to the localhost:5000/ the next page
    except requests.exceptions.HTTPError as error:
        error.code
        #download_image(src)
        #return render_template("index.html", result=str(error)) #else error is thrown


def download_image(url):
    print(url)
    try:
        image_name = url[url.rfind("/")+1:] #finds the last slash and extracts character till the end
        if(str(image_name).find("?")!=-1):    #if question mark is found
            image_name = url[url.rfind("/")+1:+url.rfind("?")] #extract characters till the question mark.
            print(image_name)
        else:
            print(image_name)
        image_path = os.path.join("images/", image_name)  #the downloaded/scraped images are saved in the folder images present where the file was saved.
        urllib.request.urlretrieve(url, image_path)
        
    except ValueError:
        print("Invalid URL !")
    except:
        print("Unknown Exception" + str(sys.exc_info()[0]))   #gives information about the exception being handled.[0] gives the type of exception.


if __name__ == "__main__":
    ic.run()
