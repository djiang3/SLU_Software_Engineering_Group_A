import json
import sys

def merge(data_A, data_B):
    new_list = list()

    for tweetA in data_A:
        new_list.append(tweetA)

    for tweetB in data_B:
        new_list.append(tweetB)

    return new_list


def check_integrity(json_file):
    print "\nOpening the json file..."
    file = open(json_file)
    print "json opened successfully!\n"

    print "Loading the json file..."
    data = json.load(file)
    print "json loaded successfully!\n"

    cnt = 0
    for line in data: cnt+=1

    print "Your json file has", cnt ,"items.\n"


def main():
    if(len(sys.argv) < 2):

        print '\nusage: json_toolkit.py [-m fileA fileB newFileName] [-c file]'
        print '-m: merges fileA and fileB, then outputs the combined file as newFileName'
        print '-c: checks the integrity of file\n'
        sys.exit(1)
    
    if(sys.argv[1] == '-m'):

        if(len(sys.argv) < 5):
            print '\nusage: [fileA fileB newFileName]\n'
            sys.exit(1)

        file_A = open(sys.argv[1],'r')
        file_B = open(sys.argv[2],'r')
        
        data_A = json.load(file_A)
        data_B = json.load(file_B)

        new_out = json.dumps(merge(data_A,data_B))
        
        new_file = open(argv[4],'w')
        new_file.write(new_out)

        file_A.close()
        file_B.close()
        new_file.close()

    elif(sys.argv[1] == '-c'):

        if (len(sys.argv) < 3):
            print '\nusage: [file]\n'
            sys.exit(1)

        check_integrity(sys.argv[2])


if __name__ == '__main__':
    main()
