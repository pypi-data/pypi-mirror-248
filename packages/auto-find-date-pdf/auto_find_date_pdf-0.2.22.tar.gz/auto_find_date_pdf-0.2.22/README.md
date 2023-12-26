# Simple use Date and text parsing from pdf rtf and images (with use of call back function)

This is a simple package provided by Marvsai healthcare LTD. It can find any format regular dates in a str 
as python Datetime objects.

Easy to use method


` def find_dates(file_contents: str): `

      Find any dates in a large python string usually taken from a file or pdf

      Args:
          file_contents (str): The string in which to find any format of dates


      Returns:
          List[datetime.datetime]: A list of datetime objects the latest can be found using max()


Optimised replacement of multiple strings in a string

` replace_multiple_strings(input_string, replacements_dict) ` 

    Replace multiple strings in the input string using a dictionary of replacement pairs.

    Args:
        input_string (str): The string in which to replace the substrings.
        replacements_dict (dict): A dictionary of replacement pairs, where the keys are the
            substrings to be replaced and the values are the replacement strings.

    Returns:
        str: The input string with all instances of the substrings replaced with their
            corresponding replacement strings.
    """
Easy to use extraction of text from PDF or RTF files:

`def extract_rtf_pdf(name: str, get_ai_text:Callable=None)->str:`
 
      Find text from pdf and rtf

      Args:
          name (str): The string in which to find any format of dates
          get_ai_text: call back function that can call google vision api or AWS or Azure equivalents for text extraction
          Called for images and image PDFs.

      Returns:
          List[datetime.datetime]: A list of datetime objects the latest can be found using max()
      """