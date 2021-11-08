import pygsheets
from pygsheets import DataRange
import pandas as pd
import os
import sys

root = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(root)

from normalize import *




all_ner_types = ["DISH", "STORE", "BRAND", "CATEGORY", "LOCATION", "COOK", "INGREDIENT"]

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
    # cur_res = get_sheet_by_name(name)
    # try:
    #     wks = sh.worksheet_by_title(name)
    # except:
    #     wks =  sh.add_worksheet(name)
    # for term in addterms:
    #     cur_res.add(term)
    # newdf = pd.DataFrame(list(cur_res).sort())
    # wks.clear()
    # wks.set_dataframe(newdf,(1,1),fit=True,nan="")

    adddf = pd.DataFrame(addterms)
    try:
        wks = sh.worksheet_by_title(name)

        row_num = wks.rows
        wks.set_dataframe(adddf,(row_num,1),fit=True,nan="",copy_head=False)
    except:
        wks = sh.add_worksheet(name,rows=len(adddf)+1,cols=20)
        wks.set_dataframe(adddf,(1,1),fit=True,nan="",copy_head =False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tn","--table_name")
    parser.add_argument("-itf","--input_file")
    parser.add_argument("-otf", "--output_file", help="specify the output file")
    parser.add_argument("-c", "--command", choices=['load', 'upload'],default="load")
    parser.add_argument("-nt", "--ner_type", default="all")
    parser.add_argument("-nn","--need_normlize",type=bool,default=True)
    parser.add_argument("-t", "--type", choices=['none', 'excel'], default='none', help='下载文件格式')
    args = parser.parse_args()

    client = pygsheets.authorize(service_file="common_tools/pygooglesheet.json")
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





