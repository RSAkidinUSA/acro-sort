#!/usr/bin/python3
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: %s file0 [file2 ..]" % (sys.argv[0], ))
        exit(-1)
    for i in sys.argv[1:]:
        try:
            fi = open(i, "r")
        except Exception as e:
            print("Unable to open %s: %s" % (i, e))
            continue
        acros = dict()
        key = ''
        brack_cnt = 0
        err = False
        for line in fi.readlines():
            line = line.rstrip('\n')
            brack_cnt += line.count('{')
            brack_cnt -= line.count('}')
            if "DeclareAcronym" in line:
                if brack_cnt != 1:
                    print("Error: file improperly formatted")
                    err = True
                    break
                else:
                    key = line.split('{')[1].split('}')[0]
                    if key in acros:
                        print("Error: reused key!")
                        err = True
                        break
                    acros[key] = ''
            elif brack_cnt > 0:
                acros[key] = acros[key] + '\n' + line

        fi.close()
        if err:
            continue
        a_s = {x: acros[x] for x in sorted(acros)}
        fo = open(i + ".sorted", "w")
        for key in a_s:
            fo.write("\\DeclareAcronym{%s}{%s\n}\n" % (key, a_s[key]))
        fo.close()


if __name__ == '__main__':
    main()
