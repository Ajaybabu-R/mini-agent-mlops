def compliance_check(docs):

    for doc in docs:
        if "Chemical" in doc:
            return "Requires hazardous material compliance check."

    return "No special compliance required."
