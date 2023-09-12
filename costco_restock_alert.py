from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
import time
import os
from dotenv import load_dotenv

# load environment files
load_dotenv()

# URLs and Constants
chocolate_product_url = "https://www.costco.ca/.product.1485984.html"
vanilla_product_url = "https://www.costco.ca/.product.1627201.html"
product_name_xpath = '"//*[@id="product-details"]/div[1]/div/div[1]/h1"'
product_price_xpath = '//*[@id="pull-right-price"]/span[1]'
product_status_xpath = '//*[@id="add-to-cart-btn"]'
out_of_stock = 'Out of Stock'

desired_price = 100.0 
recipient_email = os.getenv("RECEIVER_EMAIL_ADDRESS")
sender_email = os.getenv("SENDER_EMAIL_ADDRESS")
sender_password = os.getenv("SENDER_EMAIL_PASSWORD")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

def send_email(subject, message):
    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Log in to your email account
        server.login(sender_email, sender_password)
        
        # Compose the email message
        email_message = f"Subject: {subject}\n\n{message}"
        
        # Send the email
        server.sendmail(sender_email, recipient_email, email_message)
        
        # Close the server connection
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_price(product_url, product_name):
    try:        
        driver = start_selenium()
        driver.get(product_url)
        time.sleep(5)
        # driver.get_screenshot_as_file("screenshot.png")
        
        # Extract the product title, price, and availability
        product_price = driver.find_element(By.XPATH, product_price_xpath).text
        product_availability = driver.find_element(By.XPATH, product_status_xpath).get_attribute("value")
        
        print(f"Price: ${product_price}")
        print(f"Availability: {product_availability}")
        
        if product_availability != out_of_stock:
           send_email(f"Restock Alert: {product_name}", f"The price of {product_name} is now ${product_price}. It is in stock at {product_url}.")
        else:
            print(f"{product_name} is not in stock.")

        # Close selenium 
        driver.close()
    except Exception as e:
        print(f"Error checking price: {e}")
        
def start_selenium(): 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver 

if __name__ == "__main__":
    while True:
        check_price(product_url=chocolate_product_url, product_name='Chocolate Milk Protein')
        check_price(product_url=vanilla_product_url, product_name="Vanilla Milk Protein")
        time.sleep(1800)  # Sleep for half an hour
