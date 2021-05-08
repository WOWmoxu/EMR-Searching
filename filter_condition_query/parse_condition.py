#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding:utf-8 -*-
'''
@File : parse_condition.py
@Link :    
@name_explain :   _list(list类型); _int(int类型); _str(string类型); _set(set类型)
@Description :
@Modify Time         @Author    @Version    
---------------      -------    --------
2021/5/6 13:29      zc         1.0         
'''

import demjson

condition_str = '[{"necessary_condition":{"all":{"姓名":[],"性别":["男"],"年龄":[[<50],[>20]],"否定症状":[["发热"],["冒冷汗"],["打寒战"]],"否定疾病":[["发烧"],["感冒"]],"否定手术治疗":[],"否定非手术治疗":[],"否定药品":[["板蓝根"]],"科室":[],"部位对应症状":[[["左上肢","水肿","疼痛"],["骶尾部皮肤","破溃","流脓"]]],"精神特征对应结果":[],"生理特征对应结果":[],"生理指标对应数量":[],"肯定症状":[["头痛"],["头晕"],["恶心"],["呕吐"]],"肯定疾病":["脑震荡"],"肯定手术治疗":[],"肯定非手术治疗":[],"肯定药品名":["布洛芬"]},"zs":{"时间":[],"肯定症状":[],"否定症状":[],"部位对应症状":[]},"xbs":{"否定症状":[],"否定疾病":[],"否定手术治疗":[],"否定非手术治疗":[],"否定药品":[],"科室":[],"部位对应症状":[],"精神特征对应结果":[],"生理特征对应结果":[],"生理指标对应数量":[],"肯定症状":[["头痛"],["头晕"],["恶心"],["呕吐"]],"肯定疾病":[],"肯定手术治疗":[],"肯定非手术治疗":[],"肯定药品名":[]}}},{"sufficient_condition":{"all":{"姓名":[],"性别":[],"年龄":[],"否定症状":[],"否定疾病":[],"否定手术治疗":[],"否定非手术治疗":[],"否定药品":[],"科室":[],"部位对应症状":[],"精神特征对应结果":[],"生理特征对应结果":[],"生理指标对应数量":[],"肯定症状":[["头痛"],["头晕"],["恶心"],["呕吐"]],"肯定疾病":[],"肯定手术治疗":[],"肯定非手术治疗":[],"肯定药品名":[]},"zs":{"时间":[],"肯定症状":[],"否定症状":[],"部位对应症状":[]},"xbs":{"否定症状":[],"否定疾病":[],"否定手术治疗":[],"否定非手术治疗":[],"否定药品":[],"科室":[],"部位对应症状":[],"精神特征对应结果":[],"生理特征对应结果":[],"生理指标对应数量":[],"肯定症状":[["头痛"],["头晕"],["恶心"],["呕吐"]],"肯定疾病":[],"肯定手术治疗":[],"肯定非手术治疗":[],"肯定药品名":[]}}}]'


def get_condition(condition_str):
    """
    将条件json字符串转化为object
    :param condition_str:
    :return: condition_object
    """
    # json_str = demjson.encode(condition_str)
    condition_object = demjson.decode(condition_str)

    return condition_object


def parse_condition(condition_object):
    """
    解析条件
    :param condition_object:
    :return:
    """
    necessary_condition = condition_object[0]['necessary_condition']
    sufficient_condition = condition_object[1]['sufficient_condition']

    return necessary_condition, sufficient_condition


condition_object = get_condition(condition_str)
necessary_condition, sufficient_condition = parse_condition(condition_object)


def parse_nc():
    """
    解析必要条件
    :param necessary_condition:
    :return:
    """
    all = necessary_condition['all']  # 全域条件
    zs = necessary_condition['zs']  # 主诉条件
    xbs = necessary_condition['xbs']  # 现病史条件

    # 获取过滤后的条件
    all_conditions = filter_condition(all)
    zs_conditions = filter_condition(zs)
    xbs_conditions = filter_condition(xbs)

    return all_conditions, zs_conditions, xbs_conditions


def filter_condition(condition):
    """
    解析全域条件
    :param all:
    :return:
    """
    result_condition = dict()

    for key, value in condition.items():
        if value != []:
            result_condition[key] = value

    return result_condition


# if __name__ == "__main__":
#     condition_object = query_nc(necessary_condition)
