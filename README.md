# scraper-arxiv

Scraper to obtain title, authors, subjects, abstract and date from Arxiv papers.

To run in bg from ssh:

```bash
nohup python3 scraper.py &
```

To check progress in logs:

```bash
grep Count:: scraping.log
```
