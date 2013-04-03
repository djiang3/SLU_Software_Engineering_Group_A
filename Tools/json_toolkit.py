import json
import sys

def merge(data_A, data_B):
    new_list = list()

    for tweetA in data_A:
        new_list.append(tweetA)

    for tweetB in data_B:
        new_list.append(tweetB)

    return new_list


def main():
    if(len(sys.argv) < 2):
        print 'usage error: json_toolkit.py'
        print 'input two files to process'
        sys.exit(1)
    
    file_A = open(sys.argv[1],'r')
    file_B = open(sys.argv[2],'r')
    
    data_A = json.load(file_A)
    data_B = json.load(file_B)

    new_out = json.dumps(merge(data_A,data_B))
    
    new_file = open('combined.json','w')
    new_file.write(new_out)

    file_A.close()
    file_B.close()
    new_file.close()


if __name__ == '__main__':
    main()
