def main():
    with open("temp.txt") as f:
        data=f.readlines()
        sum=0
        ser:dict[str,list]={}
        for i in data:
            ser[i]=[]
            for j in i:
                if j.isnumeric():
                    ser[i].append(int(j))
        sum=0
        for i in ser.values():
            sum+=i[0]*10+i[-1]
        print(sum )

if __name__=='__main__':
    main()