https://github.com/Software-Engineering-Jagiellonian

INTRODUCTION:
- what it is
- how it works
- why useful for frege
- frege use cases
- links:
https://docs.mergestat.com/
https://github.com/mergestat/mergestat
https://hub.docker.com/r/mergestat/mergestat

INSTALLATION:

Query 0 (Using docker):
docker run mergestat/mergestat -h

- Default current working directory / --repo
- --format json / csv

OTHER TOOLS:

App: https://app.mergestat.com/w/public
FREGE-MERGESTAT: docker exec -it frege-mergestat-service bash
cd /app

QUERING:

Filtering:

Query 1 (Using docker)
docker run mergestat/mergestat summarize commits --repo "https://github.com/mergestat/mergestat"

GO INSIDE FREGE-MERGESTAT
docker exec -it frege-mergestat-service bash
cd /app

Query 2:
# Only show stats for commits that modify markdown files
mergestat summarize commits %.md --repo "https://github.com/mergestat/mergestat"

Query 3:
# Only show stats for commits that modified cmd/root.go
mergestat summarize commits cmd/root.go --repo "https://github.com/mergestat/mergestat"

Query 4:
mergestat summarize commits %.py --repo "https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git"

Query 5:
mergestat summarize commits % --repo "https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git"

Filtering with time range:

Query 6:
# Only show stats for commits authored in the 30 day period, starting 60 days ago
mergestat summarize commits --start "-600 days" --end "-300 days" --repo "https://github.com/mergestat/mergestat"

Query 7:
mergestat summarize commits % --start "-7 days" --repo "https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git" --json

Reference (using app):

Query 1:
SELECT * FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')

Query 2:
SELECT * FROM refs('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')

Query 3:
SELECT * FROM stats('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')

Query 4:
SELECT * FROM files('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
SELECT * FROM files('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git', '1c039fc399afe939b3ff6d7416f305cb4cd28959')

Query 5:
SELECT * FROM blame('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git', 'HEAD', 'README.md')

Usefull examples:

Query 1:
SELECT * FROM refs('https://github.com/mergestat/mergestat')
WHERE type = 'tag' AND name LIKE 'v%'

Query 2:
SELECT author_name, count(*)
FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
WHERE parents < 2 -- ignore merge commits
GROUP BY author_name ORDER BY count(*) DESC

Query 3:
SELECT author_name, count(*)
FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
WHERE parents < 2 -- ignore merge commits
AND (message LIKE '%fix%'
OR message LIKE '%Fix%')
GROUP BY author_name ORDER BY count(*) DESC

Query 4:
SELECT author_name, message
FROM commits('https://github.com/Software-Engineering-Jagiellonian/django-celery-frege-poc.git')
WHERE (message LIKE '%fix%'
OR message LIKE '%Fix%')

FREGE-MERGESTAT!!!

POST http://localhost/mergestat
BODY: {
    "query": "\"SELECT author_name, count(*) FROM commits('https://github.com/mergestat/mergestat') WHERE parents < 2 GROUP BY author_name ORDER BY count(*) DESC\" -f json"
}

