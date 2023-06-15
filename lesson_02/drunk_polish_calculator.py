def op_plus(x, y):
    return x + y

def op_minus(x, y):
    return y - x

def op_multiply(x, y):
    return x * y

def op_divide(x, y):
    return x / y

def main():
    operators = {'+': op_plus,
             '-': op_minus,
             '*': op_multiply,
             '/': op_divide}

    stack = []
    input_string = input("Expression with space delimiter:").strip().split()
    for token in input_string:
        if token in operators:
            op = operators[token]
            x, y = stack.pop(), stack.pop()
            stack.append(op(x, y))
        else:
            stack.append(float(token))
    print(stack[0])

if __name__ == '__main__':
    main()


