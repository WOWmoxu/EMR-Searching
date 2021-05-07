#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding:utf-8 -*-
'''
@File : invoke_query.py
@Link :    
@name_explain :   _list(list类型); _int(int类型); _str(string类型); _set(set类型)
@Description :
@Modify Time         @Author    @Version    
---------------      -------    --------
2021/4/30 10:37      zc         1.0         
'''

from connection_neo4j import connection_neo4j
from parse_condition import parse_nc


def query_nc():
    """
    必要条件查询
    :return:
    """
    all_conditions, zs_conditions, xbs_conditions = parse_nc()
    query_all(all_conditions)


def query_all(all_conditions):
    """
    解析查询必要条件
    :param necessary_condition:
    :return:
    """
    # 拼接SQL
    head_sql = "MATCH "
    tail_sql = "WHERE "

    # 遍历条件字典
    for key, value in all_conditions.items():
        if key == '姓名':
            sql_part = 'm_r.name=' + value[0]
        elif key == '性别':
            sql_part = '(m_r:medical_record)-[:肯定关系]->(xb:cxbmc),'
            sql_part2 = 'xb.name=' + value[0]
        elif key == '年龄':
            sql_part = 'm_r.age_year' + value[0]
        elif key == '否定症状':
            for i,content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(sys%s:symptoms_node),'%i
                sql_part2 = ''


def query_sc(sufficient_condition):
    """
    解析查询充分条件
    :param sufficient_condition:
    :return:
    """

query_nc()