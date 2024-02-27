import re

def contains_trigonometric_function(string):
    trig_functions = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc']
    pattern = '|'.join(trig_functions)
    regex = re.compile(pattern)
    return bool(regex.search(string))

def extract_x_part(expression):
    x_parts = re.findall(r'(?<!\w)(x\s*[+-]\s*\d+|\bx\b)(?!\w)', expression)
    return x_parts

def get_text_after_substring(main_string, substring):
    index = main_string.find(substring)
    if index != -1:  # If substring is found
        return main_string[index + len(substring):]
    else:
        return None


def main():
    equation = "-2*x^4 + (3+2)*4*(x + 3)^2 - sin(x) + cot(x + 12) + csc(2x)"
    #equation = "4*x^2"
    x = 'x' # this codes assumes tha the variable is x
    print(f"Input: {equation}")
    scope = "global"
    curr = 0 
    terms = []
    currentTerm = ''
    equation = equation.replace("-", "+ -") 
    while curr < len(equation): 
        if equation[curr] == "(":
            scope = "local"
        if equation[curr] == ")":
            scope = "global"
        if (not equation[curr] in ["+"]) or scope == "local":
            currentTerm += equation[curr] 
        elif (equation[curr] == "+") and scope == "global":
            terms.append(currentTerm.strip().replace(" ", ""))
            currentTerm = ''
        if curr == len(equation) - 1:
            terms.append(currentTerm.strip().replace(" ", ""))
            currentTerm = ''

        curr += 1
    terms = [i for i in terms if i]
    finalTerms = []
    for i in terms:
        if contains_trigonometric_function(i):
            if "sin" in i:
                i = i.replace("sin", "cos")
            elif "cos" in i:
                i = i.replace("cos", "-sin")
            elif "tan" in i:
                i = i.replace("tan", "sec^2")
            elif "cot" in i:
                i = i.replace("cot", "-csec^2")
            elif "csc" in i:
                a = get_text_after_substring(i, "csc")
                if i[0] == "-":
                    i = "cosec" + a + "cot" + a 
                else: 
                    i = "-cosec" + a + "cot" + a
            elif "sec" in i:
                a = get_text_after_substring(i, "sec1")
                if i[0] == "-":
                    i = "sec" + a + "tan" + a 
                else: 
                    i = "-sec" + a + "tan" + a
                
            finalTerms.append(i)
        else:
            coeff = i.split("*")
            coeff = [eval(i) for i in coeff if not x in i]
            product = 1 
            for num in coeff:
                product *= num

            power = 1
            if not i == i.split('^')[-1]:
                power = i.split("^")[-1] 
            xp = extract_x_part(i)[0]
            if len(xp) > 1:
                xp = "(" + xp + ")"
            
            new = f'{int(product) * int(power)}*{xp}^{int(power) - 1}'
            finalTerms.append(new)
    
    print("Derivative", " + ".join(finalTerms))

if __name__ == "__main__":
    main()
