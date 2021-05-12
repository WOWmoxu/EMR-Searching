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

graph = connection_neo4j


def query_nc():
    """
    必要条件查询
    :return:
    """
    all_conditions, zs_conditions, xbs_conditions, grs_conditions = parse_nc()
    # all_sql = sql_all(all_conditions)
    # all_patient_list = graph.run(all_sql)

    zs_sql = sql_zs(zs_conditions)
    zs_patient_list = graph.run(zs_sql)

    xbs_sql = sql_xbs(xbs_conditions)
    xbs_patient_list = graph.run(xbs_sql)

    grs_sql = sql_xbs(grs_conditions)
    grs_patient_list = graph.run(grs_sql)


def sql_all(all_conditions):
    """
    解析查询必要条件
    :param necessary_condition:
    :return:
    """
    # 拼接SQL
    sql_str = "MATCH (m_r:medical_record)-[:`肯定关系`]->(brh:cbrh), {} WHERE {} RETURN DISTINCT brh.name"
    sql_part = ""
    sql_part2 = ""
    # 遍历条件字典
    for key, value in all_conditions.items():
        if key == '姓名' and value != []:
            sql_part += 'm_r.name="%s" AND ' % value[0]
        elif key == '性别' and value != []:
            xb_list = []
            for content in value:
                xb_list += content
            sql_part += "(m_r)-[:`肯定关系`]->(xb:cxbmc),"
            sql_part2 += 'xb.name In %s AND ' % xb_list
        elif key == '年龄' and value != []:
            for i, content in enumerate(value):
                sql_part2 += 'm_r.age_year%s AND ' % content[0]
        elif key == '否定症状' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`否定关系`]->(not_sys%s:symptom_node),' % i
                sql_part2 += 'not_sys%s.name="%s" AND ' % (i, content[0])
        elif key == '否定疾病' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`否定关系`]->(not_dis%s:disease_node),' % i
                sql_part2 += 'not_dis%s.name="%s" AND ' % (i, content[0])
        elif key == '否定手术治疗' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`否定关系`]->(not_o_t:operation_treatment_node),' % i
                sql_part2 += 'not_o_t%s.name="%s" AND ' % (i, content[0])
        elif key == '否定非手术治疗' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`否定关系`]->(n_o_t:not_operation_treatment_node),' % i
                sql_part2 += 'n_o_t%s.name="%s" AND ' % (i, content[0])
        elif key == '否定药品' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`否定关系`]->(not_drug%s:drug_node),' % i
                sql_part2 += 'not_drug%s.name="%s" AND ' % (i, content[0])
        elif key == '科室' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(ks:cksmc),' % i
                sql_part2 += 'ks%s.name="%s" AND ' % (i, content[0])
        elif key == '部位对应症状' and value != []:
            for i, content in enumerate(value):
                # for j, child_content in enumerate(content):
                sql_part += '(m_r)-[:`肯定关系`]->(b_p%s:body_parts_node)-[:`肯定关系`]->(b_p_sys%s:symptom_node),' % (
                    i, i)
                sql_part2 += 'b_p%s.name = "%s" AND b_p_sys%s.name IN %s  AND ' % (i, content[0], i, content[1:])
        elif key == '精神特征对应结果' and value != []:
            # *********
            pass
        elif key == '生理特征对应结果' and value != []:
            # *********
            pass
        elif key == '生理指标对应数值' and value != []:
            for i, content in enumerate(value):
                p_i_name = physiological_indicators_dict(content[0])
                s_name = p_i_name[1:]
                sql_part += "(m_r)-[:`肯定关系`]->(%s:physiological_indicators_node)," % s_name
                sql_part2 += "%s.name='%s' AND " % (s_name, p_i_name)
                for value in content[1:]:
                    sql_part2 += "%s.value%s AND " % (s_name, value)
        elif key == '肯定症状' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(sym%s:symptom_node),' % i
                sql_part2 += 'sym%s.name IN %s AND ' % (i, content)
        elif key == '肯定疾病' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(dis%s:disease_node),' % i
                sql_part2 += 'dis%s.name="%s" AND ' % (i, content[0])
        elif key == '肯定手术治疗' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(o_t:operation_treatment_node),' % i
                sql_part2 += 'o_t%s.name="%s" AND ' % (i, content[0])
        elif key == '肯定非手术治疗' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(y_n_o_t%s:not_operation_treatment_node),' % i
                sql_part2 += 'y_n_o_t%s.name="%s"  AND ' % (i, content[0])
        elif key == '肯定药品' and value != []:
            for i, content in enumerate(value):
                sql_part += '(m_r)-[:`肯定关系`]->(drug%s:drug_node),' % i
                sql_part2 += 'drug%s.name="%s" AND ' % (i, content[0])

    result_str = sql_str.format(sql_part[:-1], sql_part2[:-4])
    print(result_str)
    return result_str


def sql_zs(zs_condition):
    """
    查询主诉
    :param zs_condition:
    :return:
    """
    sql_str = "MATCH (zs:czs)<-[:`肯定关系`]-(m_r:medical_record)-[:`肯定关系`]->(brh:cbrh) WHERE %s RETURN DISTINCT brh"
    sql_part = ""

    for i, content in zs_condition:
        sql_part += "zs.org_txt=~'.*%s.*'"%content[0]

    result_str = sql_str%sql_part
    print(result_str)
    return result_str


def sql_xbs(xbs_condition):
    """
    查询现病史
    :param xbs_condition:
    :return:
    """
    sql_str = "MATCH (xbs:cxbs)<-[:`肯定关系`]-(m_r:medical_record)-[:`肯定关系`]->(brh:cbrh) WHERE %s RETURN DISTINCT brh"
    sql_part = ""

    for i, content in xbs_condition:
        sql_part += "xbs.org_txt=~'.*%s.*'" % content[0]

    result_str = sql_str % sql_part
    print(result_str)
    return result_str


def sql_grs(grs_condition):
    """
    查询个人史
    :param grs_condition:
    :return:
    """

    sql_str = "MATCH (grs:cgrs)<-[:`肯定关系`]-(m_r:medical_record)-[:`肯定关系`]->(brh:cbrh) WHERE %s RETURN DISTINCT brh"
    sql_part = ""

    for i, content in grs_condition:
        sql_part += "grs.org_txt=~'.*%s.*'" % content[0]

    result_str = sql_str % sql_part
    print(result_str)
    return result_str



def query_sc(sufficient_condition):
    """
    解析查询充分条件
    :param sufficient_condition:
    :return:
    """


def physiological_indicators_dict(p_i_name):
    """
    生理指标对应数值字典
    :param p_i_name:
    :return:
    """
    p_i_dict = {
        '身高': 'nsg',
        '体重': 'ntz',
        '体温': 'ntw',
        '呼吸频率': 'nhxpl',
        '脉率': 'nml',
        '收缩压': 'nssy',
        '舒张压': 'nszy'
    }

    p_i_value = p_i_dict[p_i_name]
    return p_i_value


def filter_patient(all_patients=None, zs_patients=None, xbs_patients=None, grs_patients=None):
    """
    过滤条件
    :param all_patients:
    :param zs_patients:
    :param xbs_patients:
    :param grs_patients:
    :return:
    """





query_nc()
