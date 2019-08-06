import cx_Oracle


def sql_insert_form_item_value(answer, create_form, get_if_form_item, get_if_form_item_value, index):
    insert_form_item_value = """
                            INSERT INTO SOLUTION_FORM.FORM_ITEM_VALUE (
                            ID
                            ,FORM_ITEM_ID
                            ,CODE
                            ,SORTCODE
                            ,TEXT
                            ,NOTE
                            ,BALL
                            ,STATUS
                            ,IS_DEFAULT
                            ,NAME
                            ,ROOT_ID
                            ,IGNORE_TEXT
                            ) VALUES (
                            '{form_item_value}'
                            ,'{form_item}'
                            ,'{code}'
                            , {sort_code}
                            ,'{answer}'
                            ,''
                            ,NULL
                            ,1
                            ,0
                            ,'{name_answer}'
                            ,''
                            ,NULL
                            )
                            """.format(form_item=get_if_form_item,
                                       form_item_value=get_if_form_item_value,
                                       answer=answer, name_answer=answer, code=index, sort_code=index)
    create_form.execute(insert_form_item_value)
    create_form.execute('COMMIT')


def sql_insert_form_item(create_form, id, index, item_name):
    insert_form_item = """
                DECLARE rc pkg_global.ref_cursor_type;
                BEGIN
                p_content.save_form_item(
                    NULL
                    , NULL
                    , '{id}'
                    , NULL
                    , NULL
                    , '{code}'
                    , {sortcode}
                    , {type}
                    , {type_value}
                    , NULL
                    , 0.0
                    , '{item_name}'
                    , NULL
                    , 1
                    , ''
                    , {type_value}
                    , {type_element_data}
                    , {is_multi}
                    , NULL
                    , NULL
                    , NULL
                    , ''
                    , ''
                    , 0
                    , 0
                    , 0
                    , ''
                    , 0
                    , NULL
                    , ''
                    , 0
                    , NULL
                    , rc);
                    COMMIT;
                    END;
                    """.format(item_name=item_name[1],
                               id=id, code=index,
                               sortcode=index,
                               type=item_name[0],
                               type_value=item_name[2],
                               is_multi=item_name[3],
                               type_element_data=item_name[5])
    create_form.execute(insert_form_item)


def sql_create_children_form(connection, parent_id, protocol_name):
    code_form = sql_next_code_form(connection)
    add_form = "DECLARE rc pkg_global.ref_cursor_type;" \
               " BEGIN p_content.save_form(" \
               "NULL, NULL, {parent_id}, {id_form}," \
               " {id_form},  '{protocol_name}', ''," \
               " 0.0, 1, 1, 0," \
               " '', NULL, NULL, 0, 0, rc);COMMIT;END;".format(protocol_name=str(protocol_name),
                                                               id_form=code_form, parent_id=parent_id)
    connection.cursor().execute(add_form)
    return  code_form

def sql_create_parent_form(connection, protocol_name):
    code_form = sql_next_code_form(connection)
    add_form = "DECLARE rc pkg_global.ref_cursor_type;" \
               " BEGIN p_content.save_form(" \
               "NULL, NULL, NULL, {id_form}," \
               " {id_form},  '{protocol_name}', ''," \
               " 0.0, 1, 1, 0," \
               " '', NULL, NULL, 0, 0, rc);COMMIT;END;".format(protocol_name=str(protocol_name),
                                                               id_form=code_form)
    connection.cursor().execute(add_form)
    return code_form


def sql_next_code_form(connection):
    code_form = int(connection.cursor().execute("SELECT MAX(TO_NUMBER(code)) + 1 FROM solution_form.form where"
                                                " trim(TRANSLATE(code, '0123456789-,.', ' ')) is null").fetchone()[
                        0])
    return code_form


def sql_get_id_form(connection, id_form):
    parent_id = int(connection.cursor().execute("select id from SOLUTION_FORM.FORM where "
                                                "code ='{id_form}' and rownum = 1".format(id_form=id_form)).fetchone()[
                        0])
    return parent_id


def sql_get_all_protocol_folders(connection):
    list_folders = connection.cursor().execute("""select code, TEXT from solution_form.form where ROOT_ID is NULL""").fetchall()
    for code, value in enumerate(list_folders):
        print(str(code) + ':' + str(value))

def connect_MED():
    connection = cx_Oracle.connect('solution_med/elsoft@med')
    print(connection.version)
    return connection