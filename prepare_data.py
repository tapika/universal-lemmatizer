import sys
import os

ID,FORM,LEMMA,UPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

def read_conllu(f):
    sent=[]
    comment=[]
    for line in f:
        line=line.strip()
        if not line: # new sentence
            if sent:
                yield comment,sent
            comment=[]
            sent=[]
        elif line.startswith("#"):
            comment.append(line)
        else: #normal line
            sent.append(line.split("\t"))
    else:
        if sent:
            yield comment, sent


def create_data(args):

    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    f_inp=open(args.output+".input","wt",encoding="utf-8")
    f_out=open(args.output+".output","wt",encoding="utf-8")

    counter=0
    for comm, sent in read_conllu(open(args.file,"rt",encoding="utf-8")):
        
        for token in sent:
        
            # TODO null nodes
            
            if "-" in token[ID]:
                continue
            
            lemma=" ".join(c for c in token[LEMMA].replace(" ","$@@$")) # replace whitespace with $@@$
            wordform=" ".join(c for c in token[FORM].replace(" ","$@@$"))
            
            tags=[]
            if args.extra_tag!="":
                tags.append(args.extra_tag)
            tags.append("UPOS="+token[UPOS])
            
            for t in token[FEAT].split("|"):
                if t=="_":
                    tags.append("FEAT="+t)
                else:
                    tags.append(t)
            tags=" ".join(tags)
            print(wordform,tags,file=f_inp)
            print(lemma,file=f_out)
            counter+=1
    print("Done, files have",counter,"examples.",file=sys.stderr)



if __name__=="__main__":

    import argparse

    parser = argparse.ArgumentParser(description='')
    g=parser.add_argument_group("Reguired arguments")
    
    g.add_argument('-f', '--file', type=str, help='Input file name')
    g.add_argument('-o', '--output', type=str, help='Output file name, will create file extentions .input and .output')
    g.add_argument('--extra_tag', type=str, default="", help='extra tag, for example mark autoencoding training examples')
    
    args = parser.parse_args()

    create_data(args)