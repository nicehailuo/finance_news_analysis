# -*- coding: utf-8 -*-

import os
import mysql_config
from sqlalchemy import func


def query_table_count(db_session, class_type):
    ''' 获取某张表的行数 '''
    count = db_session.query(func.count('*')).select_from(class_type).scalar()
    return count


def query_web_id(db_session, website_name):
    ''' 通过网站名称查找网站id '''
    web_id = db_session.select(
        mysql_config.TABLE_WEB,
        "web_name=\"%s\"" % website_name,
        False,
        "web_id")
    return web_id


def insert_new_website(db_session, website_name, web_address):
    ''' 插入一个新的网站名称 '''
    web_id = db_session.insertOne(
        mysql_config.TABLE_WEB,
        web_name=website_name,
        web_address=web_address)
    return web_id
    pass


def query_file_id(db_session, filename):
    ''' 通过文件名查找文件id '''
    file_id = db_session.select(
        mysql_config.TABLE_NEWS_FILE,
        "file_name=\"%s\"" % filename,
        False,
        "news_file_id")
    return file_id
    pass


def insert_new_filename(db_session, web_id, filename):
    ''' 插入一个新的文件名称 '''
    news_file_id = db_session.insertOne(
        mysql_config.TABLE_NEWS_FILE,
        web_id=web_id,
        file_storage_location=filename,
        file_name=os.path.split(filename)[-1])
    return news_file_id


def query_page_id(db_session, page_level, page_name):
    ''' 通过板块级数和板块名称查找板块id '''
    page_id = db_session.select(
        mysql_config.TABLE_PAGE,
        "page_name=\"%s\" and page_level=%d" % (page_name, page_level),
        False,
        "page_id")
    return page_id


def insert_page(db_session, section_name, level, parent_section=None):
    ''' 插入版面数据 '''
    page_id = 0
    if parent_section is None:
        page_id = db_session.insertOne(
            mysql_config.TABLE_PAGE,
            page_name=section_name, page_level=level)
    else:
        page_id = db_session.insertOne(
            mysql_config.TABLE_PAGE,
            page_name=section_name, page_level=level,
            parent_page_id=parent_section)
    if page_id == 0:
        page_id = query_page_id(db_session, level, section_name)
    return page_id
