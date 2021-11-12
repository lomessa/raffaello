import pygsheets
from pygsheets import DataRange
import pandas as pd
import os
import sys

cur_path =  os.path.dirname(__file__)

from normalize import *




all_ner_types = ["DISH", "STORE", "BRAND", "CATEGORY", "LOCATION", "COOK", "INGREDIENT"]


def get_first_empty_colum(sheet):
    row_num = sheet.rows
    i=0
    drange = DataRange(start='A1', end='A' + str(row_num), worksheet=sheet)
    while i<row_num:
        cur_text = drange.cells[i][0].value_unformatted
        if cur_text != "":
            i = i + 1
        else:
            break
    return i+1

def delet_data(name,delet_items):
    # cur_items = list(get_sheet_by_name(name))
    # reserved_items = []
    # for item in cur_items:
    #     if item not in delet_items:
    #         reserved_items.append(item)
    # df = pd.DataFrame(reserved_items.sort())
    # df[2] = name
    delet_rows = []
    cur_sheet = sh.worksheet_by_title(name)
    row_num = cur_sheet.rows
    drange = DataRange(start='A1', end='A' + str(row_num), worksheet=cur_sheet)
    flag = 0
    for i in range(row_num):
        cur_text = drange.cells[i][0].value_unformatted
        if cur_text in delet_items:
            delet_rows.append(i-flag+1)
            flag = flag + 1
    for row in delet_rows:
        cur_sheet.delete_rows(row,number=1)


def get_sheet_by_name(name,need_normlize=True):
    entitys = set([])
    try:
        cur_sheet = sh.worksheet_by_title(name)
    except:
        print("no sheet for %s",name)
        return set([])
    row_num = cur_sheet.rows
    drange = DataRange(start='A1',end='A'+str(row_num),worksheet=cur_sheet)
    for i in range(row_num):
        cur_text = drange.cells[i][0].value_unformatted
        if need_normlize:
            cur_text = normlize_en(str(cur_text))
        if cur_text != "":
            entitys.add(cur_text)
    return entitys

def upload_data_by_name(name,addterms,normlize=True):
    adddf = pd.DataFrame(addterms)
    adddf[2] = name
    try:
        wks = sh.worksheet_by_title(name)
        row_num = get_first_empty_colum(wks)
        wks.set_dataframe(adddf,(row_num,1),fit=True,nan="",copy_head=False)
    except:
        wks = sh.add_worksheet(name,rows=len(adddf)+1,cols=20)
        wks.set_dataframe(adddf,(1,1),fit=True,nan="",copy_head =False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tn",  "--table_name")
    parser.add_argument("-itf", "--input_file")
    parser.add_argument("-otf", "--output_file", help="specify the output file")
    parser.add_argument("-c",   "--command", choices=['load', 'upload', 'delete'],default="load")
    parser.add_argument("-nt",  "--ner_type", default="all")
    parser.add_argument("-nn",  "--need_normlize", type=bool,default=True)
    parser.add_argument("-t",   "--type", choices=['none', 'excel'], default='none', help='下载文件格式')
    args = parser.parse_args()

    client = pygsheets.authorize(service_file=os.path.join(cur_path,"pygooglesheet.json"))
    sh = client.open(args.table_name)

    if args.command == "load":
        res = {}
        if args.ner_type == "all":
            for name in all_ner_types:
                print(name)
                res[name] = get_sheet_by_name(name)
        else:
            res[args.ner_type] = get_sheet_by_name(args.ner_type)

        with codecs.open(args.output_file,'w','utf-8') as writer:
            for k in res.keys():
                tmplist = res[k]
                for tmpitem in tmplist:
                    writer.write(tmpitem + "\t" + k + "\n")
                print("load %d item for type %s" %(len(tmplist),k))
    elif args.command == "upload":
        toadd = {}
        with codecs.open(args.input_file,'r','utf-8') as reader:
            for line in reader.readlines():
                terms = line.strip().split("\t")
                if len(terms) != 2:
                    continue
                if terms[1] in toadd:
                    toadd[terms[1]].append(terms[0])
                else:
                    toadd[terms[1]] = [terms[0]]
        for k in toadd.keys():
            upload_data_by_name(k,toadd[k])
    elif args.command == "delete":
        todelet = {}
        with codecs.open(args.input_file, 'r', 'utf-8') as reader:
            for line in reader.readlines():
                terms = line.strip().split("\t")
                if len(terms) != 2:
                    continue
                if terms[1] in todelet:
                    todelet[terms[1].strip()].append(terms[0].strip())
                else:
                    todelet[terms[1].strip()] = [terms[0].strip()]
        for k in todelet.keys():
            delet_data(k,todelet[k])






