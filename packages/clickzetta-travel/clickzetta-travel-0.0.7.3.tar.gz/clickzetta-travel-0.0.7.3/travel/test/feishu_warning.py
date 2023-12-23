import copy
import json
import logging
import sqlite3
import time
import requests

sqlite_db_file_path_mysql_cdp_mdm = 'sqlite_gray_mysql_cdp_mdm_mysql.db'
sqlite_db_file_path_mysql_log_analysis = 'sqlite_gray_mysql_log_analysis_mysql.db'
sqlite_db_file_path_mysql_other = 'sqlite_gray_mysql_other_mysql.db'
sqlite_db_file_path_pg = 'sqlite_gray_pg_pg.db'
feishu_hook = 'https://open.feishu.cn/open-apis/bot/v2/hook/eede3a36-15e8-40b0-a5e9-cfc43573a2de'
headers = {
    "Content-Type": "application/json",
}
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mysql_cdp_mdm_abnormal_tables = set()
mysql_log_analysis_abnormal_tables = set()
mysql_other_abnormal_tables = set()
data_hr = {
    "tag": "hr"
}
pg_recovery_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "pg 恢复表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}
mysql_other_recovery_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_other 恢复表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}

mysql_cdp_mdm_recovery_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_cdp_mdm 恢复表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}

mysql_log_analysis_recovery_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "green",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_log_analysis 恢复表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}
pg_abnormal_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "pg 新增异常表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}
mysql_other_abnormal_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_other 新增异常表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}

mysql_cdp_mdm_abnormal_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_cdp_mdm 新增异常表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}
mysql_log_analysis_abnormal_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_log_analysis 新增异常表",
                    "tag": "lark_md"
                }
            },

        ]
    }
}
pg_data_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "pg 数据校验结果",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": "源端表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "目标表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅源端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅目标端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
        ]
    }
}
mysql_other_data_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_other 数据校验结果",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": "源端表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "目标表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅源端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅目标端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
        ]
    }
}

mysql_cdp_mdm_data_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_cdp_mdm 数据校验结果",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": "源端表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "目标表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅源端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅目标端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
        ]
    }
}

mysql_log_analysis_data_content = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "content": "XSY_数据校验报警",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "content": "mysql_log_analysis 数据校验结果",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": "源端表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "目标表",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅源端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "仅目标端存在ID",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": "缺失次数",
                            "tag": "lark_md"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
        ]
    }
}


def get_data_content(cursor, template, source_count, dest_count, type):
    try:
        abnormal_tables = set()
        cursor.execute(
            f'select * from xsy_validation where cast(only_source_max_times_id as integer) >= {source_count}  order by cast(only_source_max_times_id as integer) desc')
        result_source = cursor.fetchall()
        count = 0
        for row in result_source:
            abnormal_tables.add(row[2].strip())
            count += 1
            if count >= 20:
                continue
            data = {
                "tag": "div",
                "fields": [
                ]
            }
            items_source = row[7].split('|')
            only_in_source_ids = []
            only_in_source_times = []
            only_in_dest_ids = []
            only_in_dest_times = []
            for item in items_source:
                if len(item) == 0:
                    continue
                times_and_ids = item.split('-')
                if int(times_and_ids[0]) >= int(source_count):
                    ids = times_and_ids[1].split(',')
                    if len(ids) >= 2:
                        ids_str = ','.join(ids[:1]) + '...}'
                    else:
                        ids_str = times_and_ids[1]
                    only_in_source_ids.append(ids_str)
                    only_in_source_times.append(times_and_ids[0])
            items_dest = row[8].split('|')
            for item in items_dest:
                if len(item) == 0:
                    continue
                times_and_ids = item.split('-')
                if int(times_and_ids[0]) >= int(source_count):
                    ids = times_and_ids[1].split(',')
                    if len(ids) >= 2:
                        ids_str = ','.join(ids[:1]) + '...}'
                    else:
                        ids_str = times_and_ids[1]
                    only_in_dest_ids.append(ids_str)
                    only_in_dest_times.append(times_and_ids[0])
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[1]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[2]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_source_ids) + '\n' if len(only_in_source_ids) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_source_times) + '\n\n' if len(only_in_source_times) > 0 else '无',
                    "tag": "lark_md"
                }
            })

            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_dest_ids) if len(only_in_dest_ids) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_dest_times) if len(only_in_dest_times) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            template['card']['elements'].append(data)
            template['card']['elements'].append(data_hr)
        cursor.execute(
            f'select * from xsy_validation where cast(only_dest_max_times_id as integer) >= {dest_count}  order by cast(only_dest_max_times_id as integer) desc')
        result_dest = cursor.fetchall()
        for row in result_dest:
            if row[2].strip() in abnormal_tables:
                continue
            abnormal_tables.add(row[2].strip())
            count += 1
            if count >= 20:
                continue
            data = {
                "tag": "div",
                "fields": [
                ]
            }
            items_source = row[7].split('|')
            only_in_source_ids = []
            only_in_source_times = []
            only_in_dest_ids = []
            only_in_dest_times = []
            for item in items_source:
                if len(item) == 0:
                    continue
                times_and_ids = item.split('-')
                if int(times_and_ids[0]) >= int(dest_count):
                    ids = times_and_ids[1].split(',')
                    if len(ids) >= 2:
                        ids_str = ','.join(ids[:1]) + '...}'
                    else:
                        ids_str = times_and_ids[1]
                    only_in_source_ids.append(ids_str)
                    only_in_source_times.append(times_and_ids[0])
            items_dest = row[8].split('|')
            for item in items_dest:
                if len(item) == 0:
                    continue
                times_and_ids = item.split('-')
                if int(times_and_ids[0]) >= int(dest_count):
                    ids = times_and_ids[1].split(',')
                    if len(ids) >= 2:
                        ids_str = ','.join(ids[:1]) + '...}'
                    else:
                        ids_str = times_and_ids[1]
                    only_in_dest_ids.append(ids_str)
                    only_in_dest_times.append(times_and_ids[0])
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[1]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[2]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_source_ids) + '\n' if len(only_in_source_ids) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_source_times) + '\n\n' if len(only_in_source_times) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_dest_ids) if len(only_in_dest_ids) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '\n'.join(only_in_dest_times) if len(only_in_dest_times) > 0 else '无',
                    "tag": "lark_md"
                }
            })
            template['card']['elements'].append(data)
            template['card']['elements'].append(data_hr)
        cursor.execute(f"select * from xsy_validation where last_check_status = 'UN_DONE';")
        result_dest = cursor.fetchall()
        for row in result_dest:
            if row[2].strip() in abnormal_tables:
                continue
            abnormal_tables.add(row[2].strip())
            data = {
                "tag": "div",
                "fields": [
                ]
            }
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[1]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": f"**{row[2]}**",
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '无',
                    "tag": "lark_md"
                }
            })
            data['fields'].append({
                "is_short": True,
                "text": {
                    "content": '无',
                    "tag": "lark_md"
                }
            })
            template['card']['elements'].append(data)
            template['card']['elements'].append(data_hr)
        if len(abnormal_tables) > 0:
            r = requests.post(feishu_hook, headers=headers, data=json.dumps(template))
            logger.info(r.json)
        # abnormal tables handle
        new_abnormal_tables = set()
        if type == 1:
            new_abnormal_tables = abnormal_tables - globals()['mysql_cdp_mdm_abnormal_tables']
        elif type == 2:
            new_abnormal_tables = abnormal_tables - globals()['mysql_log_analysis_abnormal_tables']
        elif type == 3:
            new_abnormal_tables = abnormal_tables - globals()['mysql_other_abnormal_tables']
        elif type == 4:
            new_abnormal_tables = abnormal_tables - globals()['pg_abnormal_tables']

        temp_mysql_cdp_mdm_abnormal_content = copy.deepcopy(mysql_cdp_mdm_abnormal_content)
        temp_mysql_log_analysis_abnormal_content = copy.deepcopy(mysql_log_analysis_abnormal_content)
        temp_mysql_other_abnormal_content = copy.deepcopy(mysql_other_abnormal_content)
        temp_pg_abnormal_content = copy.deepcopy(pg_abnormal_content)

        if len(new_abnormal_tables) > 0:
            if type == 1:
                temp_mysql_cdp_mdm_abnormal_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(new_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_mysql_cdp_mdm_abnormal_content))
            elif type == 2:
                temp_mysql_log_analysis_abnormal_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(new_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers,
                                  data=json.dumps(temp_mysql_log_analysis_abnormal_content))
            elif type == 3:
                temp_mysql_other_abnormal_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(new_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_mysql_other_abnormal_content))
            elif type == 4:
                temp_pg_abnormal_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(new_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_pg_abnormal_content))

        recovered_abnormal_tables = set()
        if type == 1:
            recovered_abnormal_tables = globals()['mysql_cdp_mdm_abnormal_tables'] - abnormal_tables
        elif type == 2:
            recovered_abnormal_tables = globals()['mysql_log_analysis_abnormal_tables'] - abnormal_tables
        elif type == 3:
            recovered_abnormal_tables = globals()['mysql_other_abnormal_tables'] - abnormal_tables
        elif type == 4:
            recovered_abnormal_tables = globals()['pg_abnormal_tables'] - abnormal_tables

        temp_mysql_cdp_mdm_recovery_content = copy.deepcopy(mysql_cdp_mdm_recovery_content)
        temp_mysql_log_analysis_recovery_content = copy.deepcopy(mysql_log_analysis_recovery_content)
        temp_mysql_other_recovery_content = copy.deepcopy(mysql_other_recovery_content)
        temp_pg_recovery_content = copy.deepcopy(pg_recovery_content)

        if len(recovered_abnormal_tables) > 0:
            if type == 1:
                temp_mysql_cdp_mdm_recovery_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(recovered_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_mysql_cdp_mdm_recovery_content))
            elif type == 2:
                temp_mysql_log_analysis_recovery_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(recovered_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers,
                                  data=json.dumps(temp_mysql_log_analysis_recovery_content))
            elif type == 3:
                temp_mysql_other_recovery_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(recovered_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_mysql_other_recovery_content))
            elif type == 4:
                temp_pg_recovery_content['card']['elements'].append({
                    "tag": "div",
                    "text": {
                        "content": '\n'.join(recovered_abnormal_tables),
                        "tag": "lark_md"
                    }
                })
                r = requests.post(feishu_hook, headers=headers, data=json.dumps(temp_pg_recovery_content))

        if type == 1:
            globals()['mysql_cdp_mdm_abnormal_tables'] = abnormal_tables
        elif type == 2:
            globals()['mysql_log_analysis_abnormal_tables'] = abnormal_tables
        elif type == 3:
            globals()['mysql_other_abnormal_tables'] = abnormal_tables
        elif type == 4:
            globals()['pg_abnormal_tables'] = abnormal_tables

    except Exception as e:
        logger.error(e)
        raise e


def check():
    while True:
        try:
            logger.info('start check at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            with sqlite3.connect(sqlite_db_file_path_mysql_cdp_mdm) as conn:
                mysql_cdp_mdm_temp = copy.deepcopy(mysql_cdp_mdm_data_content)
                cursor = conn.cursor()
                get_data_content(cursor, mysql_cdp_mdm_temp, 2, 2, 1)

            with sqlite3.connect(sqlite_db_file_path_mysql_log_analysis) as conn:
                mysql_log_analysis_temp = copy.deepcopy(mysql_log_analysis_data_content)
                cursor = conn.cursor()
                get_data_content(cursor, mysql_log_analysis_temp, 2, 2, 2)

            with sqlite3.connect(sqlite_db_file_path_mysql_other) as conn:
                mysql_other_temp = copy.deepcopy(mysql_other_data_content)
                cursor = conn.cursor()
                get_data_content(cursor, mysql_other_temp, 2, 2, 3)

            with sqlite3.connect(sqlite_db_file_path_pg) as conn:
                pg_temp = copy.deepcopy(pg_data_content)
                cursor = conn.cursor()
                get_data_content(cursor, pg_temp, 2, 2, 4)


            # break
            time.sleep(7200)
        except Exception as e:
            print(e)
            time.sleep(1200)


if __name__ == '__main__':
    check()
