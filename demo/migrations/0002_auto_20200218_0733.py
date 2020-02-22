# Generated by Django 2.2.10 on 2020-02-17 09:44

from django.db import migrations


def non_null_count(*values):
    none_values = [i for i in values if i == None]

    return len(none_values)


DB_FUNCTIONS = {
    "postgresql": {
        "forward": lambda conn, cursor: cursor.execute(
            """
            CREATE OR REPLACE FUNCTION public.non_null_count(VARIADIC arg_array ANYARRAY)
              RETURNS BIGINT AS
              $$
                SELECT COUNT(x) FROM UNNEST($1) AS x
              $$ LANGUAGE SQL IMMUTABLE;
        """
        ),
        "reverse": lambda conn, cursor: cursor.execute(
            """
            DROP FUNCTION IF EXISTS public.non_null_count(VARIADIC arg_array ANYARRAY);
        """
        ),
    },
    "sqlite": {
        "forward": lambda conn, cursor: conn.create_function(
            "non_null_count", -1, non_null_count
        ),
        "reverse": lambda conn, cursor: conn.create_function(
            "non_null_count", -1, None
        ),
    },
    "mysql": {
        "forward": lambda conn, cursor: cursor.execute(
            """
            CREATE FUNCTION non_null_count (params JSON)
                RETURNS INT
                DETERMINISTIC
                READS SQL DATA
            BEGIN
                DECLARE n INT DEFAULT JSON_LENGTH(params);
                DECLARE i INT DEFAULT 0;
                DECLARE current BOOLEAN DEFAULT false;
                DECLARE val INT DEFAULT 0;

                WHILE i < n DO
                  SET current = if(JSON_TYPE(JSON_EXTRACT(params, concat('$[', i , ']'))) != 'NULL', true, false);
                  IF current THEN
                    SET val = val + 1;
                  END IF;
                  SET i = i + 1;
                END WHILE;
                RETURN val;
            END;
            CREATE TRIGGER demo_book_validate before INSERT ON demo_book
            FOR each row
            BEGIN
                if non_null_count(JSON_ARRAY(new.amount_off, new.percentage)) = 0
                THEN
                    signal SQLSTATE '45000' SET message_text = 'Both amount_off and percentage cannot
                    be null';
                END if;
            END;


            CREATE TRIGGER demo_book_validate_2 before UPDATE ON demo_book
            FOR each row
            BEGIN
                if non_null_count(JSON_ARRAY(new.amount_off, new.percentage)) = 0
                THEN
                    signal SQLSTATE '45000' SET message_text = 'Both amount_off and percentage cannot
                    be null';
                END if;
            END;
        """
        ),
        "reverse": lambda conn, cursor: cursor.execute(
            """
            DROP FUNCTION non_null_count;
            DROP TRIGGER demo_book_validate;
            DROP TRIGGER demo_book_validate_2;
        """
        ),
    },
}


def forwards_func(apps, schema_editor):
    conn = schema_editor.connection
    vendor = conn.vendor

    with conn.cursor() as cursor:
        func = DB_FUNCTIONS[vendor]["forward"]

        func(conn.connection, cursor)


def reverse_func(apps, schema_editor):
    conn = schema_editor.connection
    db_alias = conn.db_alias

    with conn.cursor() as cursor:
        func = DB_FUNCTIONS[db_alias]["reverse"]

        func(conn, cursor)


class Migration(migrations.Migration):
    dependencies = [
        ("demo", "0001_initial"),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
