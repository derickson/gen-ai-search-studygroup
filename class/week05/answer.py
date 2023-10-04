def annotated_entity_to_list_of_tuples(message_ner):
    # Pattern to capture content inside [text](label&value)
    pattern = r'\[(.*?)\]\((.*?)&(.*?)\)'
    
    result = []
    last_end = 0

    # Iterating over each match
    for match in re.finditer(pattern, message_ner):
        # Getting start and end index of match
        start, end = match.span()
        
        # If there's text before the match, add it to result
        if start != last_end:
            result.append((message_ner[last_end:start]))
        
        # Add the matched tuple
        label, value = match.groups()[1], match.groups()[0]
        result.append((value, label))
        
        last_end = end
    
    # If there's remaining text after the last match, add it to result
    if last_end != len(message_ner):
        result.append((message_ner[last_end:]))

    return result