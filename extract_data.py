import requests
from lxml import html, etree

def read_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.text)

    # convert to formatted HTML
    formatted_html = etree.tostring(tree, pretty_print=True, encoding="unicode")
    with open("wendys_html_content.html", "w", encoding="utf-8") as f:
        f.write(formatted_html)
    return formatted_html

def extract_data_from_html(html_content):
    dominos_list = []
    dict_data = {}
    tree = html.fromstring(html_content)
    dict_data["brand_name"] = tree.xpath("string(.//div[@class='HeroBanner-left']//h1[@class='HeroBanner-title Heading--lead'])").strip()

    dict_data["phone_no"] = tree.xpath(
        "string(.//span[@class='c-phone-number-span c-phone-main-number-span'])").replace("(", "").replace(") ", "-")

    dict_data["image_link"] = tree.xpath("string(.//div[@class='Promo-imgWrapper']//img/@data-src)")

    dict_data["map_url"] = tree.xpath("normalize-space(string(.//div[@class='c-get-directions-button-wrapper']//a/@href))")
    timeing_data = tree.xpath("//tr[@itemprop='openingHours']")

    hours_time = {}
    for data in timeing_data:
        day = data.xpath("string(.//td[@class='c-location-hours-details-row-day'])").strip()
        start_time = data.xpath("string(.//span[@class='c-location-hours-details-row-intervals-instance-open'])").strip()
        end_time = data.xpath("string(.//span[@class='c-location-hours-details-row-intervals-instance-close'])").strip()
        hours_time[day] = start_time + " to " + end_time
    dict_data["hours_time"] = hours_time

    delivery_option_data = tree.xpath("//div[@class='LocationInfo-deliveryPartnerInfo']//a[@class='LocationInfo-deliveryPartnerLink']")
    delivery_option_list = []
    for data in delivery_option_data:
        image_link = data.xpath("string(.//img[@class='LocationInfo-deliveryPartnerImg']/@src)")
        delivery_option_list.append(image_link)
    dict_data["delivery_option_image"] = delivery_option_list

    services = tree.xpath("//li[@class= 'LocationInfo-service']")
    facility_list = []
    for item in services:
        items = item.xpath('normalize-space(string(.//span[@itemprop="amenityFeature"]))')
        facility_list.append(items)
    dict_data["facility"] = facility_list
    dominos_list.append(dict_data)
    return dominos_list