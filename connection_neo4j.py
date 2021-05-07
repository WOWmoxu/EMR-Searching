#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding:utf-8 -*-
'''
@File : connection_neo4j.py
@Link :    
@name_explain :   _list(list类型); _int(int类型); _str(string类型); _set(set类型)
@Description :
@Modify Time         @Author    @Version    
---------------      -------    --------
2021/4/30 10:38      zc         1.0         
'''

import configparser
from py2neo import Graph

def read_config_params():
    """
    读取配置文件的参数
    :return:
    """

    path = 'config_params.ini'
    config = configparser.ConfigParser()
    config.read(path)
    ## 此处返回的sections list不包括 default
    print("> config sections : %s" % config.sections())
    print('neo4j.org' in config)  ## 判断配置文件中是否存在该 section
    print("> Load config file is :")
    param_dict = dict()

    for section in config.keys():
        print("[{s}]".format(s=section))
        for key in config[section]:
            param_dict[key] = config[section][key]

    return param_dict


def connection_neo4j():
    """
    连接Neo4j
    :return:
    """
    params = read_config_params()
    graph = Graph(host=params.get('host'), http_port=params.get('http_port'),
                  user=params.get('user'), password=params.get('password'))

    return graph

# connection_neo4j()









