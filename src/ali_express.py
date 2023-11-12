from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from . import variants
from . import feedback
from pprint import pprint


def AliexpressProductScraper(productId, feedbackLimit=None):
    FEEDBACK_LIMIT = feedbackLimit or 10

    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)

    # Scrape aliexpress product page for details
    browser.get(f'https://www.aliexpress.com/item/{productId}.html')
    params = browser.execute_script('return runParams;')
    if isinstance(params, str):
        aliExpressData = json.loads(params)
    else:
        aliExpressData = params
    data = aliExpressData['data']

    # Scrape the description page for the product using the description url
    descriptionUrl = data['productDescComponent']['descriptionUrl']
    browser.get(descriptionUrl)
    descriptionPageHtml = browser.page_source

    # Build the AST for the description page html content using BeautifulSoup
    soup = BeautifulSoup(descriptionPageHtml, 'html.parser')
    descriptionData = str(soup.body)

    # Fetch the adminAccountId required to fetch the feedbacks
    adminAccountId = browser.execute_script('return adminAccountId')
    browser.close()

    feedbackData = []

    if data['feedbackComponent']['totalValidNum'] > 0:
        feedbackData = feedback.get_feedback(
            data['productInfoComponent']['id'],
            adminAccountId,
            data['feedbackComponent']['totalValidNum'],
            FEEDBACK_LIMIT
        )

    # Build the JSON response with aliexpress product details
    result = {
        'title': data['productInfoComponent']['subject'],
        'categoryId': data['productInfoComponent']['categoryId'],
        'productId': data['productInfoComponent']['id'],
        'totalAvailableQuantity': data['inventoryComponent']['totalAvailQuantity'],
        'description': descriptionData,
        'orders': data['tradeComponent']['formatTradeCount'],
        'storeInfo': {
            'name': data['sellerComponent']['storeName'] if 'storeName' in data['sellerComponent'] else None,
            'companyId': data['sellerComponent']['companyId'] if 'companyId' in data['sellerComponent'] else None,
            'storeNumber': data['sellerComponent']['storeNum'] if 'storeNum' in data['sellerComponent'] else None,
            'followers': data['sellerComponent']['followingNumber'] if 'followingNumber' in data['sellerComponent'] else None,
            'ratingCount': data['sellerComponent']['positiveNum'] if 'positiveNum' in data['sellerComponent'] else None,
            'rating': data['sellerComponent']['positiveRate'] if 'positiveRate' in data['sellerComponent'] else None
        },
        'ratings': {
            'totalStar': 5,
            'averageStar': data['feedbackComponent']['averageStar'] if 'averageStar' in data['feedbackComponent'] else None,
            'totalStartCount': data['feedbackComponent']['totalValidNum'] if 'totalValidNum' in data['feedbackComponent'] else None,
            'fiveStarCount': data['feedbackComponent']['fiveStarNum'] if 'fiveStarNum' in data['feedbackComponent'] else None,
            'fourStarCount': data['feedbackComponent']['fourStarNum'] if 'fourStarNum' in data['feedbackComponent'] else None,
            'threeStarCount': data['feedbackComponent']['threeStarNum'] if 'threeStarNum' in data['feedbackComponent'] else None,
            'twoStarCount': data['feedbackComponent']['twoStarNum'] if 'twoStarNum' in data['feedbackComponent'] else None,
            'oneStarCount': data['feedbackComponent']['oneStarNum'] if 'oneStarNum' in data['feedbackComponent'] else None
        },
        'images': data['imageModule']['imagePathList'] if ('imageModule' in data and 'imagePathList' in data['imageModule']) else [],
        'feedback': feedbackData,
        'variants': variants.get(data['priceComponent']['skuPriceList']),
        'specs': data['productPropComponent']['props'],
        'currency': data['currencyComponent']['currencyCode'],
        'originalPrice': {
            'min': data['priceComponent']['origPrice']['minAmount']['value'],
            'max': data['priceComponent']['origPrice']['maxAmount']['value']
        },
        'salePrice': {
            'min': data['priceComponent']['discountPrice']['minActivityAmount']['value'] if ('minActivityAmount' in data['priceComponent']['discountPrice']) else data['priceComponent']['discountPrice']['minAmount']['value'],
            'max': data['priceComponent']['discountPrice']['maxActivityAmount']['value'] if ('maxActivityAmount' in data['priceComponent']['discountPrice']) else data['priceComponent']['discountPrice']['maxAmount']['value']
        }
    }

    return result

