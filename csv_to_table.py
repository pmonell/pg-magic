import csv
from session_inspect import Session
from sqlalchemy import Table, Column, Integer, Unicode, MetaData
import StringIO

def read_csv_headers(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        return reader.fieldnames
        
def prepare_csv(file):
    with open(file, 'r') as f:
        f.next()
        mem_str = ''
        count = 1
        for line in f:
            mem_str += str(count) + ',' + line
            count += 1
    print mem_str
    return StringIO.StringIO(mem_str)

def create_table_from_headers(name, headers):
    e = Session.engine()
    metadata= MetaData(bind=e)
    
    table = Table(name, metadata, Column('id', Integer, primary_key=True),
        *(Column(head, Unicode(255)) for head in headers))
    
    metadata.create_all()
    return 0

def get_table_mapping(table_name):
    table = Table(table_name, autoload=True, autoload_with=engine())

def copy_to_table(table_name, file):
    mem_str = prepare_csv(file)
    session = Session()
    session.copy_from(mem_str, table_name)

if __name__ == '__main__':
    name = 'website'
    #create_table_from_headers(name, read_csv_headers('website.csv'))
    copy_to_table('website', 'website.csv')
