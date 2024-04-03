# Yelp DataSet

# Restaurant Classifier and Recommender

## Project motivation / Business use case

The review website, [Yelp](https://www.yelp.com/), released an open-source datset of crowdsourced user reviews for a subset of businesses represented on the platform. This project is primarily exploratory in nature, but is focused on the use of this data in the creation of two distinct systems, with various potential customer use cases outlined below and the associated markdown files [Classifier](Classifier.md) & [Recommender](Recommender.md).

1. A **classifier** that seeks to determine if a user review belongs to a restaurant or not
2. A **recommender** that provides users with similar restaurants to ones they have scored highly in the past

## Data collection

The data comes directly from Yelp themselves as part of their [Yelp Open Dataset](https://www.yelp.com/dataset) It covers ~7M reviews from ~150k businesses in specific metropolitan areas in the United States. 
**Due to the size of the dataset, it has not been included in the repo, but can be found at the link above**
The data comes in five distinct JSON files covering various aspects of the reviews and business data:
* business.json:
  * PrimaryKey: **business_id**
  * Contains business data including location data, attributes, and categories.
* review.json:
  * PrimaryKey: **review_id**
  * Contains full review text data including the user_id that wrote the review and the business_id the review is written for.
* user.json:
  * PrimaryKey: **user_id**
  * User data including the user's friend mapping and all the metadata associated with the user.
* checkin.json:
  * PrimaryKey: **business_id**
  * Checkins on a business.
* tip.json:
  * PrimaryKey: **user_id**, **business_id**, **text**, **date**
  * Tips written by a user on a business. Tips are shorter than reviews and tend to convey quick suggestions.
* photo.json:
  * PrimaryKey: **photo_id**
  * Contains photo data including the caption and classification (one of "food", "drink", "menu", "inside" or "outside").
 
Currently, the metropolitan areas centered on Montreal, Calgary, Toronto, Pittsburgh, Charlotte, Urbana-Champaign, Phoenix, Las Vegas, Madison, and Cleveland, are included in the dataset.

I leveraged the functions in the `json_to_csv_converter_py3.py` to convert the JSON files into CSV for ease of use in EDA via the `Pandas` library. This code was referenced in Yelp's dataset documentation, and a py2 example may be found [here](https://github.com/Yelp/dataset-examples/blob/master/json_to_csv_converter.py).

In order to move quicker in EDA and creation, I limited the dataset that I was working with to only businesses in the Philadelphia metropolitan area. This narrowed the data set to ~34k businesses and ~1.6M reviews which was still sufficiently large to use in creating a robust classifer and recommender.

I wrote a number of functions in Python which aided in cleaning the data, and filtering to just the columns necessary for an initial POC. These functions can be found in the `dataprep.py` file in this repo.

As I wanted to focus primarily on free text fields for analysis, I exclusively relied on the **business** and **review** files, noting that additional information -- especially in the tip, and user datasets would be helfpul for performance improvement down the line.

## Data preparation

The following steps were completed to prepare the data for the text analysis:
1. Conversion from JSON to CSV - see section above
2. PA only - see section above
3. Unicode import issues - Various string literals had unicode characters to remove
4. String cleaning - Standard issue case and punctuation modification
5. Duplicates/NaN removed - Duplicate businesses as well as user/business/review_text combinations were present in the dataset
6. Restaurant tagging - Using the `categories` feature, tagged businesses that included "restaurants" in the cateogry. Note that this data is used in Yelp's search functionality for filtering:

![YelpRestaurantSearch](images/YelpRestaurantSearch.png)

Reviewing the output of the data showed that only businesses in the PA area remained:

![GeoDistrib](images/GeoDistrib.png)

The resulting review data showed reviews with an approx. length of 76 words with a mean 3.75 star rating:

![ReviewWords](images/ReviewWords.png)

![ReviewStars](images/ReviewStars.png)

Additionally, included business had a minimuim of 5 and a mean of 76 reviews:

![ReviewsByBusiness](images/ReviewCount.png)

# Classifier and recommender

For information regarding the classifer and recommender, see the associated Markdown files here:

[Classifier](Classifier.md)

[Recommender](Recommender.md)