import math

#base function for checking which person we are loaning to and what their credit modifier is
def loan_approval_algorithm(personal_code, loan_amount, loan_period):

    if (personal_code == 49002010965): # debt
        return ("negative",)
    elif (personal_code == 49002010976): # credit_modifier = 100
        return approval_per_person(100, loan_period)

    elif (personal_code == 49002010987): # credit_modifier = 300
        return approval_per_person(300, loan_period)

    elif (personal_code == 49002010998): # credit_modifier = 1000
        return approval_per_person(1000, loan_period)
    else:
        return ("negative", "unknown ID number")

# For a specific credit_modifier and loan period finding if we can approve a loan for this period at all. If not we find another suitable period
def approval_per_person(credit_modifier, loan_period):
    if (loan_period < 12 or loan_period > 60):
        return find_suitable_period(credit_modifier, 2000)

    # try requested period first
    result = find_max_approved(credit_modifier, loan_period)
    if result[0] != "negative":
        return result

    # fallback: find a period that works for the requested amount
    return find_suitable_period(credit_modifier, 2000)

#function for finding maximal allowed loan amount for a specific period and credit_modifier
def find_max_approved(credit_modifier, loan_period):
    # We know that a clients credit_score = (credit_modifier / loan_amount) * loan_period
    # And for loan approval credit_score has to be >= 1
    # So (credit_modifier / loan_amount) * loan_period >= 1
    # and  (credit_modifier * loan_period) / loan_amount >= 1
    # And as a conclusion for the credit score to be over 1, it has to be true that credit_modifier * loan_period >= loan_amount
    # And the maximal possible loan amount is then credit_modifer * loan_period, because if loan_amount we're bigger than that the credit_score would also be under 1
    max_amount = credit_modifier * loan_period

    # capping to constraints
    if max_amount > 10000:
        max_amount = 10000

    if max_amount < 2000:
        return ("negative", 0, loan_period)

    return ("positive", max_amount, loan_period)


# code for simply checking if a specific client will be approved for certain loan_amount and loan_period or not
def scoring_algorithm(credit_modifier, loan_amount, loan_period):
    credit_score = (credit_modifier / loan_amount) * loan_period

    if (credit_score >= 1):
        # we will round the loan_amount since loans are usually whole euro's
        return ("positive", round(loan_amount), loan_period)
    elif (credit_score < 1):
        return ("negative",0, loan_period)


# Helper function for the case when we can't provide any loan amount for the requested loan_period and need to find a new alternative period
def find_suitable_period(credit_modifier, loan_amount):
    # I use math.ceil to find the minimum period where amount divided by modifier is larger than or equal to one
    min_period = math.ceil(loan_amount / credit_modifier)

    # I check that this found period still fits between the constraints
    if min_period < 12:
        min_period = 12
    if min_period > 60:
        return ("negative",)

    return ("positive", round(loan_amount), min_period)

