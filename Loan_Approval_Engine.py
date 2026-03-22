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
    result = find_max_approved(credit_modifier, 2000, 10000, loan_period)
    if result != "negative":
        return result

    # fallback: find a period that works for the requested amount
    return find_suitable_period(credit_modifier, 2000)

#function for finding maximal allowed loan amount for a specific period and credit_modifier
# I will use binary search recursively to look for the maximum amount approved
def find_max_approved(credit_modifier, loan_amount_start, loan_amount_end, loan_period):
    # Our options for loan amounts are restricted by 2000 and 6000
    # the middle of loan_amount_start and loan_amount_end is the current amount we are checking

    # base case - if we have gotten to a place where there is no better/higher solution to look for ("all other cases" have been checked already)
    if (loan_amount_end - loan_amount_start) < 1:
        # the current loan_amount is the only possible loan we can give, so if thsi is approved it is approved. Else it is not approved
        current_approval = scoring_algorithm(credit_modifier, loan_amount_start, loan_period)
        if (current_approval[0] == "positive"):
            return current_approval
        else:
            return ("negative",)
    # Step -  Otherwise we still check if current loan would be allowed
    else:
        current_loan_amount = (loan_amount_end + loan_amount_start) / 2
        current_loan_approval = scoring_algorithm(credit_modifier, current_loan_amount, loan_period)

        if (current_loan_approval[0] == "positive"): # if current approved loan is allowed we check if a higher loan would also be approved
            larger_loan_approval = find_max_approved(credit_modifier, current_loan_amount, loan_amount_end, loan_period)
            # there is a case where no larger loan than current will be approved so we have to check if a bigger loan amount really was found

            # if there was no larger loan found
            if (larger_loan_approval[0] == "negative" or
                    # or if the larger loan that we found is still somehow smaller than the current approved loan amount
                    larger_loan_approval[0] == "positive" and current_loan_approval[1] < larger_loan_approval[1]):
                return current_loan_approval # as this is the largest approved loan we will find
            else:
                return larger_loan_approval


        elif (current_loan_approval[0] == "negative"): # if current loan was not approved we check if a lower loan will be approved
            return find_max_approved(credit_modifier, loan_amount_start, current_loan_amount, loan_period)


# code for simply checking if a specific client will be approved for certain loan_amount and loan_period or not
def scoring_algorithm(credit_modifier, loan_amount, loan_period):
    credit_score = (credit_modifier / loan_amount) * loan_period

    if (credit_score >= 1):
        return ("positive", loan_amount)
    elif (credit_score < 1):
        return ("negative",0)


# Helper function for the case when we can't provide any loan amount for the requested loan_period and need to find a new alternative period
def find_suitable_period(credit_modifier, loan_amount):
    # I use math.ceil to find the minimum period where amount divided by modifier is larger than or equal to one
    min_period = math.ceil(loan_amount / credit_modifier)

    # I check that this found period still fits between the constraints
    if min_period < 12:
        min_period = 12
    if min_period > 60:
        return ("negative",)

    return ("positive", loan_amount, min_period)

