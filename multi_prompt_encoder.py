import time
import openpyxl
import csv
import openai

openai.api_key = "[YOUR_KEY]"

# Exponential backoff parameters
max_retry_count = 5
retry_delay_base = 1
retry_delay_max = 60

justice_encoding_dict = {
    "Jay" : 1,
    "Rutledge": 2,
    "Cushing": 3,
    "Wilson": 4,
    "Blair": 5,
    "Iredell": 6,
    "Johnson": 7,
    "Paterson": 8,
    "Chase": 10,
    "Ellsworth": 11,
    "Washington": 12,
    "Moore": 13,
    "Marshall": 14,
    "Johnson": 15,
    "Livingston": 16,
    "Todd": 17,
    "Duvall": 18,
    "Story": 19,
    "Thompson": 20,
    "Trimble": 21,
    "McLean": 22,
    "Baldwin": 23,
    "Wayne": 24,
    "Taney": 25,
    "Barbour": 26,
    "Catron": 27,
    "McKinley": 28,
    "Daniel": 29,
    "Nelson": 30,
    "Woodbury": 31,
    "Grier": 32,
    "Curtis": 33,
    "Campbell": 34,
    "Clifford": 35,
    "Swayne": 36,
    "Miller": 37,
    "Davis": 38,
    "Field": 39,
    "Strong": 41,
    "Bradley": 42,
    "Hunt": 43,
    "Waite": 44,
    "Harlan": 45,
    "Woods": 46,
    "Matthews": 47,
    "Gray": 48,
    "Blatchford": 49,
    "Lamar": 50,
    "Fuller": 51,
    "Brewer": 52,
    "Brown": 53,
    "Shiras": 54,
    "Jackson": 55,
    "White": 56,
    "Peckham": 57,
    "McKenna": 58,
    "Holmes": 59,
    "Day": 60,
    "Moody": 61,
    "Lurton": 62,
    "Hughes": 63,
    "VanDevanter": 64,
    "Pitney": 66,
    "McReynolds": 67,
    "Brandeis": 68,
    "Clarke": 69,
    "Taft": 70,
    "Sutherland": 71,
    "Butler": 72,
    "Sanford": 73,
    "Stone": 74,
    "Roberts": 76,
    "Cardozo": 77,
    "Black": 78,
    "Reed": 79,
    "Frankfurter": 80,
    "Douglas": 81,
    "Murphy": 82,
    "Byrnes": 83,
    "Burton": 86,
    "Vinson": 87,
    "Minton": 89,
    "Warren": 90,
    "Harlen": 91,
    "Brennan": 92,
    "Whittaker": 93,
    "Stewart": 94,
    "Goldberg": 96,
    "Fortas": 97,
    "Marshall": 98,
    "Burger": 99,
    "Blackmun": 100,
    "Powell": 101,
    "Rehnquist": 102,
    "Stevens": 103,
    "Connor": 104,
    "Scalia": 105,
    "Kennedy": 106,
    "Souter": 107,
    "Thomas": 108,
    "Ginsburg": 109,
    "Breyer": 110,
    "Alito": 112,
    "Sotomayor": 113,
    "Kagan": 114,
    "Gorsuch": 115,
    "Kavanaugh": 116,
    "Barrett": 117
}


def split_text(raw_text):

    supreme_court_splits = []

    #petitioner_state
    index = raw_text.find(("petitioner"))

    if index == -1:
        petionerState_text = raw_text[:1000]
    else:
        petionerState_text = raw_text[:index + len("petitioner")]

    supreme_court_splits.append(petionerState_text)

    #lcDisposition
    concur_index = raw_text.rfind("concur")
    dissent_index = raw_text.rfind("dissent")
    if concur_index == -1 and dissent_index == -1:
        lcDisposition_text = raw_text[-500:]
    elif concur_index > dissent_index:
        lcDisposition_text = raw_text[concur_index - 500:concur_index]
    else:
        lcDisposition_text = raw_text[dissent_index - 500:dissent_index]
    
    supreme_court_splits.append(lcDisposition_text)


    #caseDisposition
    index = raw_text.find(("Argued"))
    if index == -1:
        caseDisposition_text = raw_text[:1000]
    else:
        caseDisposition_text = raw_text[:index + 50]
    
    supreme_court_splits.append(caseDisposition_text)

    print(caseDisposition_text)

    #precedentAlteration
    precedentAlteration_text = raw_text[:100]
    supreme_court_splits.append(precedentAlteration_text)

    #issueArea
    issueArea_text = raw_text[:300]
    supreme_court_splits.append(issueArea_text)

    #decisionDirection
    decisionDirection_text = raw_text[:500]
    supreme_court_splits.append(decisionDirection_text)

    #partyWinning
    partyWinning_text = raw_text[:100]
    supreme_court_splits.append(partyWinning_text)

    #lawType
    lawType_text = raw_text[:100]
    supreme_court_splits.append(lawType_text)

    #majOpinWriter
    index = raw_text.find(("delivered the opinion"))
    if index == -1:
        majOpinWriter_text = raw_text[:1000]
    else:
        majOpinWriter_text = raw_text[index - 100 : index + len("delivered the opinion")]
    
    supreme_court_splits.append(majOpinWriter_text)


    #chief
    index = raw_text.find(("Argued"))
    if index == -1:
        cheif_text = raw_text[:1000]
    else:
        cheif_text = raw_text[index - len("Argued") : index + 50]
    
    supreme_court_splits.append(cheif_text)
    return supreme_court_splits


def run_gpt_prompts(case_id, raw_text):
    responses = []
    
    supreme_court_splits = split_text(raw_text)

    prompt_count = 0

    for prompt in [f"""{supreme_court_splits[0]} 

                    If the petitioner of the above case originated from a distinct location, please identify it using the numerical numbering system below. The answer will almost always be 0 unless explicitly stated 

                    0: No Petitioner State Mentioned
                    1: Alabama
                    2: Alaska
                    3: American Samoa
                    4: Arizona
                    5: Arkansas
                    6: California
                    7: Colorado
                    8: Connecticut
                    9: Delaware
                    10: District of Columbia
                    11: Federated States of Micronesia
                    12: Florida
                    13: Georgia
                    14: Guam
                    15: Hawaii
                    16: Idaho
                    17: Illinois
                    18: Indiana
                    19: Iowa
                    20: Kansas
                    21: Kentucky
                    22: Louisiana
                    23: Maine
                    24: Marshall Islands
                    25: Maryland
                    26: Massachusetts
                    27: Michigan
                    28: Minnesota
                    29: Mississippi
                    30: Missouri
                    31: Montana
                    32: Nebraska
                    33: Nevada
                    34: New Hampshire
                    35: New Jersey
                    36: New Mexico
                    37: New York
                    38: North Carolina
                    39: North Dakota
                    40: Northern Mariana Islands
                    41: Ohio
                    42: Oklahoma
                    43: Oregon
                    44: Palau
                    45: Pennsylvania
                    46: Puerto Rico
                    47: Rhode Island
                    48: South Carolina
                    49: South Dakota
                    50: Tennessee
                    51: Texas
                    52: Utah
                    53: Vermont
                    54: Virgin Islands
                    55: Virginia
                    56: Washington
                    57: West Virginia
                    58: Wisconsin
                    59: Wyoming
                    60: United States
                    61: Interstate Compact
                    62: Philippines
                    63: Indian
                    64: Dakota

                    Along with the numerical answer, include an explanation of why. An example answer would be “0-The explanation is blah blah blah”. The answer must be in this format

                   """, 
                   f"""{supreme_court_splits[1]} 

                   Given the above text, What treatment did the lower court give in the disposition in this case? Please respond with a number 1-12 indicating the result, with each number corresponding to one of the options:

                    1: either stay, petition, or motion granted,
                    2: affirmed (includes modified),
                    3: reversed,
                    4: reversed and remanded,
                    5: vacated and remanded, 
                    6: affirmed and reversed (or vacated) in part, 
                    7: affirmed and reversed (or vacated) in part and remanded, 
                    8: vacated, 
                    9: petition denied or appeal dismissed, 
                    10: modify,
                    11: remand, or
                    12: unusual disposition

                    
                    Along with the numerical answer, include an explanation of why. An example answer would be “10-The explanation is blah blah blah”. The answer must be in this format
                    """,
                     f"""{supreme_court_splits[2]}
                    Given the above supreme court case, What treatment did the Supreme Court give the decision of the lower court in this case? Please respond with a number 1-12 indicating the result, with each number corresponding to one of the options:

                    1: either stay, petition, or motion granted,
                    2: affirmed (includes modified),
                    3: reversed,
                    4: reversed and remanded,
                    5: vacated and remanded, 
                    6: affirmed and reversed (or vacated) in part, 
                    7: affirmed and reversed (or vacated) in part and remanded, 
                    8: vacated, 
                    9: petition denied or appeal dismissed, 
                    10: modify,
                    11: remand, or
                    12: unusual disposition
                    
                    Along with the numerical answer, include an explanation of why. An example answer would be “10-The explanation is blah blah blah”. The answer must be in this format
                    """,
                    f"""{supreme_court_splits[3]}

                    Did this Supreme Court decision ALTER, OVERRULE, or OVERTURN precedent in the above case? Please respond with only a number 0-1 indicating the answer as defined below:
                    
                    0: This case did not alter, overrule, or overturn precedent, or
                    1: This case did alter, overrule, or overturn precedent.

                    Along with the numerical answer, include an explanation of why. An example answer would be “1-The explanation is blah blah blah”. The answer must be in this format
                    """,
                    f"""{supreme_court_splits[4]}

                    You are presented with the above text of a recent Supreme Court decision, and your task is to identify the specific issue addressed in the case. The issue can be one of the following categories:

                    1: Criminal Procedure
                    2: Civil Rights
                    3: First Amendment
                    4: Due Process
                    5: Privacy
                    6: Attorneys' or Governmental Officials' Fees or Compensation
                    7: Unions
                    8: Economic Activity
                    9: Judicial Power
                    10: Federalism
                    11: Interstate Relations
                    12: Federal Taxation
                    13: Miscellaneous
                    14: Private Law

                    Along with the numerical answer, include an explanation of why. An example answer would be “9-The explanation is blah blah blah”. The answer must be in this format 
                    """, 
                    f"""{supreme_court_splits[5]}
                    
                   The number is determined by the ideological leaning of the given case: 1 for conservative, 2 for liberal, and 3 for unspecifiable. In your determination of a case as conservative, liberal, or unspecifiable, use the following criteria:

                    1. In the context of issues pertaining to criminal procedure, civil rights, First Amendment, due
                    process, privacy, and attorneys, liberal (2)=
                    - pro-person accused or convicted of crime, or denied a jury trial
                    - pro-civil liberties or civil rights claimant, especially those exercising less protected civil rights (e.g., homosexuality)
                    - pro-child or juvenile
                    - pro-indigent
                    - pro-Indian
                    - pro-affirmative action
                    - pro-neutrality in establishment clause cases
                    - pro-female in abortion
                    - pro-underdog
                    - anti-slavery
                    - incorporation of foreign territories
                    - anti-government in the context of due process, except for takings clause cases where a progovernment, anti-owner vote is considered liberal except in criminal forfeiture cases or
                    those where the taking is pro-business
                    - violation of due process by exercising jurisdiction over nonresident
                    - pro-attorney or governmental official in non-liability cases
                    - pro-accountability and/or anti-corruption in campaign spending
                    - pro-privacy vis-a-vis the 1st Amendment where the privacy invaded is that of mental
                    incompetents
                    - pro-disclosure in Freedom of Information Act issues except for employment and student records

                    conservative (1)=the reverse of above

                    2. In the context of issues pertaining to unions and economic activity, liberal (2)=
                    - pro-union except in union antitrust where liberal = pro-competition
                    - pro-government
                    - anti-business
                    - anti-employer
                    - pro-competition
                    - pro-injured person
                    - pro-indigent
                    - pro-small business vis-a-vis large business
                    - prostate/anti-business in state tax cases
                    - pro-debtor
                    - pro-bankrupt
                    - pro-Indian
                    - pro-environmental protection
                    - pro-economic underdog
                    - pro-consumer
                    - pro-accountability in governmental corruption
                    - pro-original grantee, purchaser, or occupant in state and territorial land claims
                    - anti-union member or employee vis-a-vis union
                    - anti-union in union antitrust
                    - anti-union in union or closed shop
                    - pro-trial in arbitration

                    conservative (1)= reverse of above

                    3. In the context of issues pertaining to judicial power, liberal (2)=
                    - pro-exercise of judicial power
                    - pro-judicial "activism"
                    - pro-judicial review of administrative action

                    conservative (1)=reverse of above

                    4. In the context of issues pertaining to federalism, liberal (2)=
                    - pro-federal power
                    - pro-executive power in executive/congressional disputes
                    - anti-state

                    conservative (1)=reverse of above

                    5. In the context of issues pertaining to federal taxation, liberal (2)= 
                    - pro-United States

                    conservative (1)= pro-taxpayer

                    6. In interstate relations and private law issues, unspecifiable (3) for all such cases.

                    7. In miscellaneous, incorporation of foreign territories and executive authority vis-a-vis
                    congress or the states or judicial authority vis-a-vis state or federal legislative authority =
                    (2); legislative veto = (1).

                    Along with the numerical answer, include an explanation of why. An example answer would be “1-The explanation is blah blah blah”. The answer must be in this format
                    """,
                    f"""{supreme_court_splits[6]}
                    Give me a number that indicates whether the petitioning party (i.e., the plaintiff or the appellant) emerged victorious. Use the following criteria:

                    0:  no favorable disposition for petitioning party apparent
                    1: petitioning party received a favorable disposition
                    2: favorable disposition for petitioning party unclear

                    Along with the numerical answer, include an explanation of why. An example answer would be “1-The explanation is blah blah blah”. The answer must be in this format
                    """,
                    f"""{supreme_court_splits[7]}
                    Give me a number that corresponds to the issue area of the given case. Use the following criteria:

                    1: Constitution
                    2: Constitutional Amendment
                    3: Federal Statute
                    4: Court Rules
                    5: Other
                    6: Infrequently litigated statutes
                    8: State or local law or regulation
                    9: No Legal Provision

                    Along with the numerical answer, include an explanation of why. An example answer would be “1-The explanation is blah blah blah”. The answer must be in this format
                    """,
                    f"""{supreme_court_splits[8]}

                    Give me the name of the Supreme Court Justice who authored the above majority opinion. For example, if the text says
                    'Mr. Justice Bob delivered the opinion', the output response should be:

                    'Bob'

                    Do not add anything else to return result, it should just be the single name.

                    """,
                    f"""{supreme_court_splits[9]}

                    A supreme court case was argued and decided in this time period. What was the last name of the chief justice. Respond with only the last name. 
                    """
                    ]:
        
        for retry_count in range(max_retry_count + 1):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[{"role": "system", "content": prompt}],
                    )
                if prompt_count == 8:
                    encoding = justice_encoding_dict.get(response.choices[0].message.content)
                    responses.append(encoding)
                else:
                    responses.append(response.choices[0].message.content)

                prompt_count +=1
                break
            except openai.error.ServiceUnavailableError:
                if retry_count < max_retry_count:
                    print(f"Request failed, retrying in {retry_delay_base * (2**retry_count)} seconds...")
                    time.sleep(retry_delay_base * (2**retry_count))
            except openai.error.RateLimitError:
                if retry_count < max_retry_count:
                    print(f"Request failed, retrying in {retry_delay_base * (2**retry_count)} seconds...")
                    time.sleep(retry_delay_base * (2**retry_count))
            except openai.error.Timeout:
                if retry_count < max_retry_count:
                    print(f"Request failed, retrying in {retry_delay_base * (2**retry_count)} seconds...")
                    time.sleep(retry_delay_base * (2**retry_count))
        
    return responses

def main():
    excel_file = openpyxl.load_workbook("Data/CAP_IDs_text.xlsx")
    csv_file = open("Raw_Output/GPT_output.csv", "w", newline="")
    writer = csv.writer(csv_file, delimiter=",")

    writer.writerow(["caseId"] + ["petitionerState", 
                                   "lcDisposition", 
                                   "caseDisposition", 
                                   "precedentAlteration", 
                                   "issueArea", 
                                   "decisionDirection", 
                                   "partyWinning",
                                   "lawType",
                                   "majOpinWriter",
                                   "chief"])
    sheet = excel_file["Sheet1"]
    
    cases = 0
    for row in sheet.iter_rows(max_row=100, values_only=True):
        case_id = row[0]
        raw_text = row[1]
        responses = run_gpt_prompts(case_id, raw_text)
        writer.writerow([case_id] + responses)
        cases += 1
        print("Completed Case #" + str(cases) +"\n")

if __name__ == "__main__":
    main()
