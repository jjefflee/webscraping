import requests
from bs4 import BeautifulSoup
import plotly.express as px
from collections import Counter
import pandas as pd


def scrape_quotes(url, num_pages=10):
    all_quotes = []
    for page_num in range(1, num_pages + 1):
        page_url = f"{url}/page/{page_num}/"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('span', class_='text')
        all_quotes.extend([quote.get_text() for quote in quotes])
    return all_quotes

def author_statistics(quotes):
    author_counts = Counter()

    for quote in quotes:
        author_tag = quote.find('small', class_='author')
        
        if author_tag:
            author_name = author_tag.get_text(strip=True)
            author_counts[author_name] += 1

    print("Author Counts:", author_counts)

    if not author_counts:
        print("No authors found. Check the HTML structure.")
        return author_counts, None, None

    
    most_quotes_author = max(author_counts.items(), key=lambda x: (x[1], x[0]))[0]
    least_quotes_author = min(author_counts, key=author_counts.get)

    return author_counts, most_quotes_author, least_quotes_author




def quote_analysis(quotes):
    avg_quote_length = sum(len(quote) for quote in quotes) / len(quotes)
    longest_quote = max(quotes, key=len)
    shortest_quote = min(quotes, key=len)
    return avg_quote_length, longest_quote, shortest_quote


def tag_analysis(quotes):
    tags = [tag['content'] for quote in quotes for tag in quote.find_all('meta', attrs={'class': 'keywords'})]
    tag_counts = Counter(tags)

    print("Tag Counts:", tag_counts)

    if not tag_counts:
        print("No tags found. Check the HTML structure.")
        return tag_counts, None, None

    most_popular_tag = max(tag_counts, key=tag_counts.get, default=None)
    total_tags_used = len(tags)
    return tag_counts, most_popular_tag, total_tags_used


def visualize_top_authors(author_counts):
    top_authors = author_counts.most_common(10)

    df_top_authors = pd.DataFrame(top_authors, columns=['Author', 'Number of Quotes'])
    print("Top Authors DataFrame:")
    print(df_top_authors)

    fig = px.bar(df_top_authors, x='Author', y='Number of Quotes',
                 labels={'Number of Quotes': 'Number of Quotes'},
                 title='Top 10 Authors and Their Quotes')
    fig.show()


def visualize_top_tags(tag_counts):
    top_tags = tag_counts.most_common(10)

    df_top_tags = pd.DataFrame(top_tags, columns=['Tag', 'Number of Quotes'])
    print("Top Tags DataFrame:")
    print(df_top_tags)

    fig = px.bar(df_top_tags, x='Tag', y='Number of Quotes',
                 labels={'Number of Quotes': 'Number of Quotes'},
                 title='Top 10 Tags')
    fig.show()



def main():
    url = 'http://quotes.toscrape.com'
    quotes_html = scrape_quotes(url)
    quotes_soup = [BeautifulSoup(quote, 'html.parser') for quote in quotes_html]

    author_counts, most_quotes_author, least_quotes_author = author_statistics(quotes_soup)
    print("Author Statistics:")
    print("Number of quotes by each author:", author_counts)
    print("Author with the most quotes:", most_quotes_author)
    print("Author with the least quotes:", least_quotes_author)

    avg_quote_length, longest_quote, shortest_quote = quote_analysis(quotes_html)
    print("\nQuote Analysis:")
    print("Average length of quotes:", avg_quote_length)
    print("Longest quote:", longest_quote)
    print("Shortest quote:", shortest_quote)

    tag_counts, most_popular_tag, total_tags_used = tag_analysis(quotes_soup)
    print("\nTag Analysis:")
    print("Distribution of tags:", tag_counts)
    print("Most popular tag:", most_popular_tag)
    print("Total tags used across all quotes:", total_tags_used)

    visualize_top_authors(author_counts)
    visualize_top_tags(tag_counts)


if __name__ == "__main__":
    main()
