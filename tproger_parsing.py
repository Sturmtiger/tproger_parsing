from lxml import html
import requests


def get_page_links(page_count: int) -> list:
    """
    Returns list of page links
    """
    main_domain = 'https://tproger.ru'

    page_links = list()

    for i in range(1, page_count + 1):
        link = f'{main_domain}/page/{i}/'
        page_links.append(link)

    return page_links


def get_article_links_from_pages(page_links: list) -> list:
    """
    Returns combined list of article links on each page
    """
    article_links = list()

    for link in page_links:
        response = requests.get(link)
        content = response.content
        page_element = html.fromstring(content)
        links = page_element.xpath('//article/a[contains(@class, "article-link")]/@href')
        article_links.extend(links)

    return article_links


def get_parsed_article_data(article_links: list):
    """
    Returns parsed data of each articled
    Article data types:
    1. title(Text)
    2. body(Text)
    3. images(URLs)
    4. datePublished

    """
    parsed_data = list()

    for link in article_links:
        response = requests.get(link)
        content = response.content
        page_element = html.fromstring(content)
        parsed_article = {
            'title': page_element.xpath(
                '//article[contains(@id, "post")]//h1[contains(@class, "entry-title")]/text()'
            )[0],
            'body': ' '.join(page_element.xpath(
                '//div[1][contains(@class, "entry-content")]/descendant::text()')
            ).replace('\n', ''),
            'images': page_element.xpath(
                '//div[1][contains(@class, "entry-content")]//img[not(contains(@src, "svg"))]/@src'
            ),
            'datePublished': page_element.xpath(
                '//time[contains(@class, "entry-date")]/@datetime'
            )[0].split('T')[0]
        }
        parsed_data.append(parsed_article)

    return parsed_data


if __name__ == '__main__':
    page_links = get_page_links(3)
    article_links = get_article_links_from_pages(page_links)
    parsed_articles = get_parsed_article_data(article_links)

    from json import dump
    with open('parsed_articles.json', 'w') as file:
        dump(parsed_articles, file, ensure_ascii=False)
