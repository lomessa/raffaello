import random
import argparse
import codecs
import itertools




def random_pick(some_list,probabilities):
    x = random.uniform(0,1)
    cumulative_probability=0.0
    for item,item_probability in zip(some_list,probabilities):
        cumulative_probability+=item_probability
        if x < cumulative_probability:
            break
    return item


def random_pick_by_weight(sequence,relative_weights):
    table=[z for x,y in zip(sequence,relative_weights) for z in [x]*y]
    while True:
        yield random.choice(table)

# x=random_pick_by_weight(['a','bc','dd','zh'],[1,1,3,2])
# import itertools
# print (' '.join(itertools.islice(x,4)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-itf","--input_file",help="specify the input file")
    parser.add_argument("-otf","--output_file",help="specify the output file")
    parser.add_argument("-c","--command", choices=['sample_by_weight','sample_by_odds'])
    parser.add_argument("-l1","--sample_line", type=int,default=0)
    parser.add_argument("-l2","--weight_line", type=int,default=1)
    parser.add_argument("-s","--sample_size",type=int,default=100)
    parser.add_argument("-t","--type", choices=['replace','no_replace'], default='replace', help='replace:有放回,no_replace:无放回')
    args = parser.parse_args()

    candis = []
    weights = []

    with codecs.open(args.input_file,'r','utf-8') as reader:
        for line in reader.readlines():
            terms = line.strip().split("\t")
            if args.sample_line == 0:
                candis.append(line.strip())
            else:
                candis.append(terms[args.wsample_line-1])
            weights.append(float(terms[args.weight_line-1]))

    select_samples = []
    cur_sample = itertools.islice(candis, args.sample_size * 5)
    cur_samples = "\1".join(cur_sample).split("\1")

    if args.type == "replace":
        select_samples.append(cur_samples[:args.sample_size])
    else:
        select_samples.extend(list(set(cur_samples))[:args.sample_size])

    with codecs.open(args.output_file,'w','utf-8') as writer:
        for sample in select_samples:
            writer.write(sample + "\n")


