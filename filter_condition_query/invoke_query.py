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
            sql_part = 'm_r.name="' + value[0] + '"'
        elif key == '性别':
            sql_part = '(m_r:medical_record)-[:肯定关系]->(xb:cxbmc),'
            sql_part2 = 'xb.name="' + value[0] + '" AND'
        elif key == '年龄':
            for i, content in enumerate(value):
                sql_part2 = 'm_r.age_year' + content[0] + " AND"
        elif key == '否定症状':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(sys%s:symptom_node),' % i
                sql_part2 = 'sys%s.name="' % i + content[0] + '" AND'
        elif key == '否定疾病':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(dis%s:disease_node),' % i
                sql_part2 = 'dis%s.name="' % i + content[0] + '" AND'
        elif key == '否定手术治疗':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(o_t:operation_treatment_node),' % i
                sql_part2 = 'o_t%s.name="' % i + content[0] + '" AND'
        elif key == '否定非手术治疗':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(n_o_t:not_operation_treatment_node),' % i
                sql_part2 = 'n_o_t%s.name="' % i + content[0] + '" AND'
        elif key == '否定药品':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:否定关系]->(drug%s:drug_node),' % i
                sql_part2 = 'drug%s.name="' % i + content[0] + '" AND'
        elif key == '科室':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[肯定关系]->(ks:cksmc),' % i
                sql_part2 = 'ks%s.name="' % i + content[0] + '" AND'
        elif key == '部位对应症状':
            for i, content in enumerate(value):
                for j, child_content in enumerate(content):
                    sql_part = '(m_r:medical_record)-[肯定关系]->(b_p%s:body_parts_node)-[:肯定关系]->(sys%s:symptom_node)' % (
                    j, j)
                    sql_part2 = 'b_p.name = "' + child_content[0] + '" AND ' + 'sys.name IN {}'.format(
                        child_content[1:])
        elif key == '精神特征对应结果':
            # *********
            pass
        elif key == '生理特征对应结果':
            # *********
            pass
        elif key == '生理指标对应数值':
            # *********
            pass
        elif key == '肯定症状':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:肯定关系]->(dis%s:disease_node),' % i
                sql_part2 = 'dis%s.name="' % i + content[0] + '" AND'
        elif key == '肯定手术治疗':
            # ************
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:肯定关系]->(o_t:operation_treatment_node),' % i
                sql_part2 = 'o_t%s.name="' % i + content[0] + '" AND'
        elif key == '肯定非手术治疗':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:肯定关系]->(n_o_t:not_operation_treatment_node),' % i
                sql_part2 = 'n_o_t%s.name="' % i + content[0] + '" AND'
        elif key == '肯定药品':
            for i, content in enumerate(value):
                sql_part = '(m_r:medical_record)-[:肯定关系]->(drug%s:drug_node),' % i
                sql_part2 = 'drug%s.name="' % i + content[0] + '" AND'


def query_sc(sufficient_condition):
    """
    解析查询充分条件
    :param sufficient_condition:
    :return:
    """


query_nc()
