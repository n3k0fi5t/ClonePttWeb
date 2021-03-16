# ClonePttWeb
## Introduction
**ClonePttWeb** is a project that creates a simple clone website of [PTTWeb](https://www.ptt.cc/bbs/index.html). ClonePttWeb use Django for both frontend(Django Template subsys) and backend, [PttSpider](https://github.com/n3k0fi5t/PttSpider) to crawl the data, and Celery with RabbitMQ to handle asynchronous crawling task

## Screenshots
**Home**
- dynamic add board to crawl list (period crawl will be effective after restart Celery)
- one-click to assign temporal crawl task to specific board
![](https://github.com/n3k0fi5t/ClonePttWeb/blob/main/screenshot/home.png)

**Board**
- thumbnail of Post (display first image of post if exist)
![](https://github.com/n3k0fi5t/ClonePttWeb/blob/main/screenshot/board.png)

**Post**
![](https://github.com/n3k0fi5t/ClonePttWeb/blob/main/screenshot/post.png)

## Overview
- Based on Docker, one-click deployment
- Seperated web server, database and message broker
- Using Celery and RabbitMQ for asynchronous task that do not affect website while crawling
- Beautiful layout by Leveraging Bootstrap and Custormize Django template tag/filter

## Installation
```
docker-compose up
```
