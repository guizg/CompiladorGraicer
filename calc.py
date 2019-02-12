def calculate(text):
    c = text.replace(" ", "")
    nums = []
    ops = []
    length = len(c)
  
    i = 0
    while(i<length):
        atual = c[i]
        if atual == '+' or atual == '-':
            ops.append(atual)
            i += 1
        else:
            num = atual
            k = i + 1
            if i < (length - 1):
                
                prox = c[k]
                while (prox != '+' and prox != '-'):
                    num += prox
                    k += 1
                    if k == length:
                        break
                    prox = c[k]

            nums.append(num)
            i = k


    # print(nums)
    # print(ops)

    res = int(nums.pop(0))

    while len(nums)>0:
        n = int(nums.pop(0))
        op = ops.pop(0)


        if op == "+":
            res += n
        else:
            res -= n


    print(res)



while True:
    texto = input("Qual a string? (digite 'exit' para sair) ")
    if texto == "exit":
        break
    calculate(texto)

# calculate("789      +345  -   123")

# calculate("1+2")