import random
from fractions import Fraction

def generate_question():
    question_type = random.randrange(0,6,1)
    
    if question_type == 0:
        num1 = random.randrange(-26,26,1)
        num2 = random.randrange(-26,26,1)
        
        ans = [num1 * num2]
        question = [num1, num2]
        q_type = "mult"
        
    if question_type == 1: 
        ans = random.randrange(1, 26, 1)
        den = random.randrange(-26, 26, 1)
        num = ans * den
        
        ans = [ans]
        question = [num, den]
        q_type = "div"
 
    if question_type == 2:
        num1 = random.randrange(-16,16,1)
        num2 = random.randrange(-16,16,1)
        den1 = random.randrange(1,16,1)
        den2 = random.randrange(1,16,1)
        
        ans = Fraction(num1, den1) + Fraction(num2,den2)
        s = str(ans)
        ans = s.split("/")
        question = [num1, den1, num2, den2]
        q_type = "frac_add"
            
    if question_type == 3: 
        num1 = random.randrange(-16,16,1)
        num2 = random.randrange(-16,16,1)
        den1 = random.randrange(1,16,1)
        den2 = random.randrange(1,16,1)
        
        ans = Fraction(num1, den1) - Fraction(num2,den2)
        s = str(ans)
        ans = s.split("/")
        question = [num1, den1, num2, den2]
        q_type = "frac_sub"
        
    if question_type == 4:
        num1 = random.randrange(-16,16,1)
        num2 = random.randrange(-16,16,1)
        den1 = random.randrange(1,16,1)
        den2 = random.randrange(1,16,1)
        
        ans = Fraction(num1, den1) * Fraction(num2,den2)
        s = str(ans)
        ans = s.split("/")
        question = [num1, den1, num2, den2]
        q_type = "frac_mult"
        
    if question_type == 5:
        num1 = random.randrange(-16,16,1)
        # Prevent num2 from being 0, (which would lead to 0 div error)
        n = 0
        while n == 0:
            n = random.randrange(-16,16,1)
        num2 = n
        den1 = random.randrange(1,16,1)
        den2 = random.randrange(1,16,1)
        
        ans = Fraction(num1, den1) / Fraction(num2,den2)
        s = str(ans)
        ans = s.split("/")
        question = [num1, den1, num2, den2]
        q_type = "frac_div"
    
    # Convert to strings
    question = [str(q) for q in question]
    ans = [str(a) for a in ans]
    
    return q_type, question, ans