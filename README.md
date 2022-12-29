# Dress Up

Detect your favorite piece of clothing in a clothing store

## How to use dress-up

- Navigate to `/webscraper`
  - Run `scrape_image.py` with this command : `python scrape_image.py`
    - This file is use to download all the images from a website.
  - Run `dataset_builder.py` with this command : `python dataset_builder.py`
    - This file is use to create a dataset with labeled data from the image downloaded earlier
    - When the script is in execution, Press `1` on the image to indicate that you like the picture. Press `0` or anything else to indicate that you don't like the picture. Press `Del` to delete the image if it's a random picture.
  - Run `format_image.py` with this command : `python format_image.py`
    - This file is use to format all the image in a dataset to a fixed size. It's useful for creating the model.
- Navigate to `/model`
  - Run the `model.ipynb` file
    - This file is use to create a model based on your interest using a Convolutional Neural Network

## Disclaimer

Please note that the use of web scraping may be against the terms of service of some websites. It is the responsibility of the user to ensure that they are in compliance with the terms and policies of the websites they are scraping. This tool is provided for educational and informational purposes only, and I cannot be held responsible for any misuse or violation of terms of service.

Some website like Pinterest let you use webscraping, so you can test it with this site.
