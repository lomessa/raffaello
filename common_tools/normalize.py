import re
import unidecode
import argparse
import codecs
from enum import Enum

handleSpace = re.compile("\s+")

def normlize_en(text, tolower= True, remove_sound_mark = True):
    # text = re.sub(handleSpace," ",text)
    if tolower:
        text = text.lower()
    if remove_sound_mark:
        text = unidecode.unidecode(text)
    return text

class Command(Enum):
    normlize = 'norm'




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-itf","--input_file",help="specify the input file")
    parser.add_argument("-otf","--output_file",help="specify the output file")
    parser.add_argument("-c","--command", choices=['norm'])
    parser.add_argument("-l","--column_number",type=int,default=0, help="specify the column number")
    args = parser.parse_args()

    with codecs.open(args.output_file,'w','utf-8') as writer:
        with codecs.open(args.input_file,'r','utf-8') as reader:
            for line in reader.readlines():
                terms = line.strip().split("\t")
                if args.column_number == 0:
                    writer.write(normlize_en(line))
                else:
                    terms[args.column_number-1] = normlize_en(terms[args.column_number-1])
                    writer.write("\t".join(terms).strip()+"\n")




