from googlesearch import search
from newspaper import Article
import os

def crawl_topic(topic, num_articles=10, output_dir="data_topic"):
    os.makedirs(output_dir, exist_ok=True)
    query = f"{topic} site:healthline.com OR site:who.int OR site:mayoclinic.org OR site:webmd.com"

    results = list(search(query, num_results=num_articles))
    print(f"🔍 Found {len(results)} articles on: {topic}")

    for i, url in enumerate(results):
        try:
            article = Article(url)
            article.download()
            article.parse()

            filename = os.path.join(output_dir, f"{topic.replace(' ', '_')}_{i+1}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Title: {article.title}\n\n")
                f.write(article.text)

            print(f"✅ Saved: {filename}")

        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
