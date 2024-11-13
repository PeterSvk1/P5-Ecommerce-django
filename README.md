# Sw SHOP

## Introduction
This project is an e-commerce website built to sell star wars products. The website is for users who wants to buy variety of starwars gifts or toys from the comfort of their homes. Unlike traditional simple websites, Sw SHOP focuses on providing a convenient way for users to purchase gifts and toys from their homes.

The website is built using Django framework, and follows an agile methodology approach for development.

<p align="center">
<img src="https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/assets/readme/responsive.png">
</p>

[Live version of my project](https://swshop-c6f30bb69fd8.herokuapp.com/)
<br><br>

## Table of Contents

- [Introduction](#introduction)
- [User Experience](#user-experience)
    - [Project Goal](#project-goal)
    - [User Stories](#user-stories)
    - [Scopes](#scopes)    
    - [Agile Methodology](#agile-methodology)
- [Design](#design)
    - [Wireframes](#wireframes)
    - [Database Diagram](#database-diagram)
    - [Typography and colour scheme](#typography-and-colour-scheme)
        - [Fonts](#fonts)
        - [Colour](#colour)            
- [Features](#features)
- [Future Features](#future-features)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Python Packages](#python-packages)
- [Deployment](#deployment)
    - [Deploying on heroku](#deploying-on-heroku)
    - [Fork repository](#to-fork-this-repository)
    - [Cloning](#cloning-this-project)    
- [Credits](#credits)
- [Acknowledgments](#acknowledgements)        
    
<br>

## User Experience
<br>

### Project Goal

* The goal of SW shop is to provide a platform for users to easily order toys and other star wars products from home. The website eliminates the need for users to go out into shops and can stay home.
<br><br>

### User stories

|  | As a non-logged in user |
| --- | --- |
| 1. | I want to browse the available products and view their details without having to create an account. |
| 2. | I want to search for specific product or browse through different categories. |
| 3. | I want to easily navigate through the website and find relevant information. |
| 4. | I want to register on the website to place an order or save my shipping details. |
| 5. | I want to log in to the website once registered.  |
| 6. | I want to see newsletters on the website. |

<br>

|  | As a logged in user |
| --- | --- |
| 1. | I want to add products to my cart and place an order. |
| 2. | I want to view my order history and track the status of my orders. |
| 3. | I want to edit my profile information, such as my address and payment details. |
| 4. | I want to log out from the website. |
| 5. | I want to rate the product. |
| 6. | I want to review the product. |
| 7. | I want to add the product to my wishlist. |
| 8. | I want to contact website owners. |

<br>

|  | As a staff/superuser user |
| --- | --- |
| 1. | I want to manage the inventory of products, including adding new products and updating their details. |
| 2. | I want to manage user orders and update their status. |
| 3. | I want to manage user accounts and view their order history. |
| 4. | I want delete existing products. |
| 4. | I want to add newsletters to inform users of changes like new products and such. |


<br>

### Scopes

User Registration and Authentication
- Users can create an account and log in to the website.
- Users can reset their passwords if forgotten.
- Users need to verify their email to register to the website.

Products Catalog
- Users can browse the available products without logging in.
- Products are categorized for easy navigation.
- Users can search for specific products by name or category.
- Each product has a detailed page displaying its information.

Shopping Cart and Checkout
- Users can add products to their cart.
- Users can adjust the quantity of products in the cart or remove them.
- Users can view the contents of their cart at any time.
- Users can proceed to the checkout page to place their order.
- Users can provide their shipping information and payment details during checkout.

Order Management
- Staff users can add new products to the catalog or update existing products.
- Staff users can manage user orders and update their status.
- Staff users can view user accounts and order history.

User Profile
- Users can view and edit their profile information, including address and payment details.
- Users can view their order history.

<br>

### Agile Methodology

The development of Sw SHOP follows an agile methodology approach. The project is divided into iterations, or sprints, where each sprint focuses on delivering specific features and improvements. This allows for flexibility and adaptability throughout the development process.
All my user stories, sprint that can be accessed using GitHub Issues, which serverd as a roadmap for my development process can be found [here.](https://github.com/users/PeterSvk1/projects/5)

<br>

## Design

### Wireframes

The wireframes for this project can be accessed [here.]()
<br><br>

### Database diagram

<p align="center">
<img src="https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/assets/readme/diagram.png">
</p>

### Typography and colour scheme

#### Fonts

For fonts Iam using LATO on my website.
<p align="center">
<img src="https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/assets/readme/lato.png">
</p>

#### Colour

Colour pallet used for this website.

<p align="center">
<img src="https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/assets/readme/color.png">
</p>

## Features

Features of this project can be accessed [here.](https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/FEATURES.md)
<br><br>
* Add pagination numbers to display certain number of products per page.
* Upgrade to support social authentication in addition to normal login.
* Enable the author to edit or delete review comments.
* Allow registered users to upload profile images.
* Allow users to receive information about new products added to website via our newsletter system where then can subscribe.

## Business Model

* The business model chosen for Sw SHOP website is based on a traditional e-commerce approach, where customers have the option to make single purchases of starwars products (toys and such).
* Customers are free to explore and buy products as they desire, without any recurring commitments. The online store offers a diverse range of starwars products. The focus is on providing a seamless shopping experience, secure payment processing, and efficient order fulfillment to ensure customer satisfaction.
* Newsletter subscriptions and a Facebook page, X page are utilized as marketing strategies to promote the SW shop brand and attract customers.

##  Marketing

* The marketing strategy for Sw SHOP incorporates a Facebook business page and X page as a key component. The Facebook page serves as a platform to showcase the shop's news, promotions, and offerings, aiming to establish a positive brand image. Through consistent promotion of products and regular content updates, the page endeavors to enhance its visibility and draw in a growing customer base, encouraging them to make purchases from the online store.

Facebook page mock up:

<p align="center">
<img src="">
</p>

X page:
<p align="center">
<img src="https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/assets/readme/X.png">
</p>

## Testing

Testing of this project can be accessed [here.](https://github.com/PeterSvk1/P5-Ecommerce-django/blob/main/TESTING.md)
<br> <br>

## Technologies Used

  -  HTML 5: Provides the main structure of the website.
  -  CSS 3: Used for styling the website.
  -  Bootstrap: Used for general styling and responsiveness of the website.
  -  Python: Used for the website's backend development.
  -  JavaScript: Used for website scripts, including sending emails.
  -  Django: Used as the web framework.
  -  AWS: Used for storing the website's static files.
  -  Code institute provided database.
  -  Heroku: Used for hosting the website.
  -  GitHub: Used to store the repository.
  -  GitPod: Used as the workspace for the project.
  -  Balsamiq: Used for wireframe planning.
  -  Font Awesome: Used for icons on the website.
  -  Google Fonts: Used for fonts on the website.
  -  LucidChart: Used for creating the database diagram.
  -  Favicon.ico: Used for generating the website favicon.
  -  Coolors: Used for selecting the color palette of the project.
  -  LogoAi: Used for creating the website logo.
  -  Grammarly: Used for grammar checking all the text on the website and in the readme file.
  -  Google Chrome: Used for main testing of the website on all devices.
  -  Google Chrome Lighthouse: Used for testing the performance of each page.
  -  W3C HTML Validator: Used for validating the HTML code.
  -  Jigsaw CSS Validator: Used for validating the CSS code.
  -  Ci Python Linter: Used for validating the Python code.
  -  JSHint: Used for validating the JavaScript code.
  -  Microsoft Word: Used for testing documentation.
  -  GitHub Copilot: Used to help understand developed code.
  -  Facebook: Creating business page.
  -  Gmail: Sending and receiving emails from customers.

  ### Python packages
* asgiref==3.8.1
* boto3==1.35.44
* botocore==1.35.44
* dj-database-url==0.5.0
* Django==4.2
* django-allauth==0.57.2
* django-countries==7.2.1
* django-crispy-forms==2.3
* django-storages==1.14.4
* gunicorn==23.0.0
* jmespath==1.0.1
* oauthlib==3.2.2
* pillow==10.4.0
* psycopg2==2.9.10
* PyJWT==2.9.0
* python3-openid==3.2.0
* pytz==2024.2
* requests-oauthlib==2.0.0
* s3transfer==0.10.3
* sqlparse==0.5.1
* stripe==11.1.0

## Deployment

## Deploying on Heroku
For deployment this project on Heroku, please follow these steps:
1. Create Pipfile with all the required dependencies by running the command "pip3 > freeze > requirements.txt" in the terminal.
2. Go to the Heroku website and create a [Heroku](www.heroku.com) account if you haven't already done so.
3. Create a new app by clicking the "New" button and selecting "Create a new app".
4. Choose a name for your app and select your location.
5. Get your database from codeinstitute.
6. Back in the Heroku open settings tab and paste database url from codeinstitute and Secret key to Config Vars.
7. Go to the "Deploy" tab and click on "Connect to GitHub" to connect your Heroku app to your GitHub Depositary
8. Finally, choose the main branch for deploying. Enable automatic deployment, and then select "manual deploy" to build your app.

## To Fork this repository:
1. Navigate to GitHub project repository [P5-Ecommerce-django](https://github.com/PeterSvk1/P5-Ecommerce-django)
2. Click on the "Fork" section in the right-hand corner.
3. Select an owner for the forked repository.
4. Click "Create fork" button.

## Cloning this Project
1. Visit [P5-Ecommerce-django](https://github.com/PeterSvk1/P5-Ecommerce-django)
2. Click green button "<> Code", then "Clone or download" button and copy the URL provided.
3. Open a terminal and navigate to the directory whre you want to clone the project.
4. Type following command and paste url "git clone <url>"
5. Press Enter and the project will be cloned to you local machine.

## Credits

* https://www.youtube.com/@Codemycom Django walkthrough
* Inspiration and some of the code of this project were taken from [Code Institute walkthrough project](https://github.com/Code-Institute-Solutions/boutique_ado_v1) and fellow students at Code Institue.
* https://www.youtube.com/@KevinPowell CSS effects.


## Acknowledgements

* I want to thanks to Code Institute for learning material and support.
* Slack Code Institute community for all issues resolved and support.