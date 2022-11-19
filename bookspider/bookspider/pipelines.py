# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3


class QuanShuWangPipeline(object):
    def __init__(self):
        DBpath = os.getcwd() + '/db.sqlite3'
        self.con = sqlite3.connect(DBpath)
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        self.cur.execute("SELECT id FROM books_tag WHERE tagname = ?", (item['categoryName'],))
        tagID = self.cur.fetchone()
        if not tagID:
            self.cur.execute("INSERT INTO books_tag (tagname) VALUES (?)", (item['categoryName'],))
            self.con.commit()
            self.cur.execute("SELECT id FROM books_tag WHERE tagname = ?", (item['categoryName'],))
            tagID = self.cur.fetchone()
        tagID = tagID[0]
        print(tagID)

        self.cur.execute("SELECT id FROM books_book WHERE title = ?", (item['bookName'],))
        bookID = self.cur.fetchone()

        if not bookID:
            self.cur.execute('''
            INSERT INTO books_book (title, cover, author, intro, tag_id) VALUES (?,?,?,?,?)
            ''', (item['bookName'], item['cover'], item['author'], item['intro'], tagID))
            self.con.commit()
            self.cur.execute("SELECT id FROM books_book WHERE title = ?", (item['bookName'],))
            bookID = self.cur.fetchone()

        bookID = bookID[0]
        print(bookID)

        self.cur.execute('''INSERT INTO books_chapter (number, title, content, book_id) 
                        VALUES (?,?,?,?)''', (int(item['number']), item['chapterName'], item['chapterContent'], bookID))
        self.con.commit()
        return item

    def __del__(self):
        self.con.close()

class BiQuGePipeline(object):
    def __init__(self):
        DBpath = os.getcwd() + '/db.sqlite3'
        self.con = sqlite3.connect(DBpath)
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        # 给biquge_books表插入新的书籍元数据
        self.cur.execute("SELECT id FROM biquge_books WHERE bookName = ?", (item['bookName'],))
        bookID = self.cur.fetchone()

        if not bookID:
            self.cur.execute('''
            INSERT INTO biquge_books (bookName, author, intro, coverPath, chapterNum) VALUES (?,?,?,?,?)
            ''', (item['bookName'], item['author'], item['intro'], item['cover'], item['number']))
            self.con.commit()
            self.cur.execute("SELECT id FROM books_book WHERE bookName = ?", (item['bookName'],))
            bookID = self.cur.fetchone()

        bookID = bookID[0]
        print("the ID of %s is %d\n".format(item['bookName'], bookID))

        # 建立该书籍表，存储章节数据
        self.cur.execute('''CREATE TABLE IF NOT EXISTS ? (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            chapterName varchar(50) NOT NULL, chapterUrl varchar(100), chapterContent text NOT NULL''', (item['bookName'],))
        self.cur.commit()

        self.cur.execute('''INSERT INTO ? (chapterName, chapterUrl, chapterContent) 
                        VALUES (?,?,?)''', (item['bookName'], item['chapterName'], item['chapterContent']))
        self.con.commit()
        return item

    def __del__(self):
        self.con.close()
