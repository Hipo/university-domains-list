import sys, os, json

def _country_filter(src, scope, out):
    print(scope)

def country_filter(src, scopes, out):
    if type(scopes) == "list":
        [_country_filter(src, scope, out) for scope in scopes]
    else:
        _country_filter(src, scopes, out)


def main():
    args = []
    temp_arg = ""
    first_word = True

    for arg in sys.argv[1:]:
        temp_arg += arg if first_word else " " + arg
        first_word = False

        if arg[-1] == ",":
            args.append(temp_arg[:-1])
            temp_arg = ""
            first_word = True
    
    if temp_arg: args.append(temp_arg)
    
    if not args: return
    out = []
    
    src = None
    with open('./world_universities_and_domains.json') as src_file:
        src = json.load(src_file)
    if src is None: 
        return


if __name__ == "__main__":
    main()

    # print(sys.argv)