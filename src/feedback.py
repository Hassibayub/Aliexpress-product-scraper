import requests
from bs4 import BeautifulSoup
import faker


def getFeedbackData(feedbackHtml):
    soup = BeautifulSoup(feedbackHtml, "html.parser")
    feedbackData = []

    for element in soup.select(".feedback-list-wrap .feedback-item"):
        name = element.select_one(".user-name").text.strip()
        country = element.select_one(".user-country").text.strip()
        ratingStyle = element.select_one(".star-view > span")["style"]
        ratingStyle = ratingStyle.replace("%", "")
        rating = int(ratingStyle.split("width:")[1]) / 20

        info = {}
        for infoKey in element.select(".user-order-info > span"):
            key = infoKey.find("strong").text.strip()
            info[key] = infoKey.find("strong").extract().text.strip()

        feedbackContent = element.select_one(
            ".buyer-feedback span:first-child"
        ).text.strip()
        feedbackTime = element.select_one(
            ".buyer-feedback span:last-child"
        ).text.strip()
        feedbackTime = faker.Faker().date_time_this_decade(
            before_now=True, after_now=False
        )

        photos = [
            photo.find("img")["src"]
            for photo in element.select(".r-photo-list > ul > li")
        ]

        data = {
            "name": name,
            "displayName": faker.Faker().name(),
            "country": country,
            "rating": rating,
            "info": info,
            "date": feedbackTime,
            "content": feedbackContent,
            "photos": photos,
        }

        feedbackData.append(data)

    return feedbackData


def get_feedback(productId, ownerMemberId, count, limit):
    allFeedbacks = []
    totalPages = count // limit + (count % limit > 0)

    if totalPages > 10:
        totalPages = 10

    for currentPage in range(1, totalPages + 1):
        feedbackUrl = f"https://feedback.aliexpress.com/display/productEvaluation.htm?v=2&page={currentPage}&currentPage={currentPage}&productId={productId}&ownerMemberId={ownerMemberId}"
        feedbackResponse = requests.get(feedbackUrl)
        feedbackHtml = feedbackResponse.text

        data = getFeedbackData(feedbackHtml)
        allFeedbacks.extend(data)

    return allFeedbacks
