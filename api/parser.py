def pars_doc(document: list):
    output = []
    for text, page_nr in document:

        text = text.replace("-\n","").lower().removesuffix("\n"+ str(page_nr))

        if "\nabstract\n" in text:
            text = text[text.find("\nabstract\n"):]

        
        if "\nreferences\n" in text:
            text = text[: text.find("\nreferences\n")]
            output.append((text, page_nr))
            break
        output.append((text, page_nr))
    return output
