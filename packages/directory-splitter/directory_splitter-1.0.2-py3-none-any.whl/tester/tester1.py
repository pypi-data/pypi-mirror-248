from urllib.parse import urlparse
import argparse
parser = argparse.ArgumentParser(description="Directory splitter")
parser.add_argument("-list", "--list", help="Input file with recon data")
parser.add_argument("-output", "--output", help="Output file to store split endpoints")
args = parser.parse_args()
input_file = args.list
output_file = args.output
def print_url(input_file,output_file):
    f = open(f'{input_file}','r')
    output = []
    for url in f:
        parsed_url = urlparse(url)
        path = parsed_url.path.split('/')
        while path:
            jls_extract_var = path
            output.append(f"{parsed_url.scheme}://{parsed_url.netloc}"+'/'.join(path))
            #print(f"{parsed_url.scheme}://{parsed_url.netloc}"+'/'.join(path))
            path.pop()
    unique = []
    for i in output:
        if i in unique:
            continue
        else:
            unique.append(i)    
    out = open(f'{output_file}','w')
    for i in unique:
        print(i)
    for i in unique:
        i = i + '\n'
        out.writelines(i)
print_url(input_file,output_file)