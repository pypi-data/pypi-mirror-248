# Python functionality:
import io
import time
import math

# Import Huggingface elements:
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Textpart imports:
from .regex_expressions import text_isnotcapped
from .regex_expressions import remove_nonletters

# Import nltk for eliminating incomplete sentences:
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

# Function definition for eliminating incomplete sentences:
def get_complete_sentences(text):
    sentences = sent_tokenize(text)
    complete_sentences = [sentence for sentence in sentences if sentence[-1] in ['.', '!', '?']]
    return ' '.join(complete_sentences)

def summarize_public_Huggingface_textsplitter(self, text: str, verbose_option: int) -> str:
    """
    This function takes a certain amount of text and uses The Huggingface API
    to summarize that tekst. Key parameters are the maximum number of words in the summary.
    These parameters are stored in the textsplitter-class.

    NOTE: The text should preferably keep as many newline characters
    as possible, so be sure to add them when appending a textcontent-array to text.

    # Parameters:
    text: str: the text that has to be summarized (possible a long string).
    verbose_option: int: 0: then nothing will be printed. higher numbers will print in-between stages in the terminal.
    # Return: str: the summary of the text.
    """
    
    # ---------------------------------------------------------------------

    # Declare variables we need:
    TheSummary = ""
    textpiece = text
    
    # If this is the first call that we make, reset the trackers for the rate limit:
    if (self.callcounter==0):
        self.api_rate_starttime = time.time()
        self.api_rate_currenttime = 0.0
        self.api_rate_currenttokens = 0
        self.api_rate_currentcalls = 0
        self.api_totalprice = 0.0
        self.api_wrongcalls_duetomaxwhile = 0

    # Eliminate breaks from the string:
    textpiece_nobreaks = textpiece.replace("\n"," ")
    textpiece_nobreaks = textpiece_nobreaks.strip()
    length_textpiece = len(textpiece_nobreaks.split())

    # Manage temperature settings. each time we retry, we want to raise temperature a little to
    # allow for more variations, so the probability increases that the next call will be accepted.
    Base_Temperature = self.LanguageTemperature
    Base_SummaryLength = self.MaxSummaryLength
        
    # Use a while-loop to call to Huggingface:
    Response_IsOK = False
    WhileCounter = 0
    while (not(Response_IsOK))and(WhileCounter<self.MaxCallRepeat):
            
        # Begin with managing the while-counter:
        WhileCounter = WhileCounter + 1

        # Convert Base temperature into actual temperature using the while-counter:
        Actual_Temperature = Base_Temperature + 0.05*(WhileCounter-1)
        if (Actual_Temperature>0.95): Actual_Temperature = 0.95

        # Also continuously proloung the allowed summary length, so that there is more space to
        # remove capped text and still have something left:
        Actual_Summary_Length = round(Base_SummaryLength*(1.0 + 0.2*(WhileCounter-1)))
            
        # Log if we actually hit the maximum number of loops:
        if (WhileCounter==self.MaxCallRepeat):
            self.api_wrongcalls_duetomaxwhile = self.api_wrongcalls_duetomaxwhile + 1
                
            # Log this case:
            if (verbose_option>=0):
                if isinstance(self.logfile, io.TextIOBase):
                    if self.logfile.writable():
                        self.logfile.write("This is the last time we can attempt to summarize the textpiece. We will keep the outcome no matter what!")
                
            # print it:
            if (verbose_option>=0):
                print(" ==> This is the last time we can attempt to summarize the textpiece. We will keep the outcome no matter what!")
            
        # Before making the call, we will measure time and rate to manage the rate limit of the API:
        self.api_rate_currenttime = time.time() - self.api_rate_starttime
        self.api_rate_currentcalls = self.api_rate_currentcalls + 1
        self.callcounter = self.callcounter + 1
            
        # Sleep if we passed the rate limit:
        if (self.api_rate_currentcalls>self.ratelimit_calls):
            # Then, sleep for the amount of time that we still have left in our window:
            if (self.api_rate_currenttime<=self.ratelimit_timeunit):
                print("===> textsplitter.summarize() will sleep for " + str(self.ratelimit_timeunit - self.api_rate_currenttime) + " seconds to prevent a RateLimitError. Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls))
                time.sleep(self.ratelimit_timeunit - self.api_rate_currenttime)
            
        # When sufficient time has passed, we will reset the counters:
        if ((time.time() - self.api_rate_starttime)>self.ratelimit_timeunit): # Should always be the case after a sleep!
            print(" ===> textsplitter.summarize() has reset the rate-limit counters after " + str(self.ratelimit_timeunit) + " seconds. and Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls))
            self.api_rate_starttime = time.time()                                                       # In seconds!
            self.api_rate_currenttime = 0.0                                                             # In seconds!
            self.api_rate_currentcalls = 1                                                              # We haven't made the actual call, so we must include the future call-to-be-made.
            
        # Give some general output on rate limit tracking:
        if (verbose_option>0):
            print("RATE LIMIT TRACKING: Time = " + str(time.time()) + " and Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls) + " and Total Calls = " + str(self.callcounter))
            
        # Then, actually make the call. Surround it by try-except block,
        # so we can keep on trying if it fails:
        huggingface_call_succeeded = True
        response = ""
            
        try:

            # Define inputs-tensor:
            inputs = self.huggingface_tokenizer(textpiece_nobreaks, return_tensors="pt",max_length=512, truncation=True)

            # Call the summarize-LLM:
            summary_ids = self.huggingface_model.generate(inputs["input_ids"], max_length=Actual_Summary_Length,length_penalty=2.0, num_beams=4, early_stopping=True, do_sample=True, temperature=Actual_Temperature)
                    
        except Exception as huggingface_exception:
                
            # Then, begin by marking that we caught an exception:
            huggingface_call_succeeded = False
                
            # Print it:
            print(" ==> The Huggingface API raised the following exception:")
            print(huggingface_exception)
            print("")
            print(" ==> No problem, we will just try again until we succeed; managing the API rate limit of course.")
            print("")
                
            # Log our data:
            if (verbose_option>=0):
                if isinstance(self.logfile, io.TextIOBase):
                    if self.logfile.writable():
                        self.logfile.write("Huggingface Call " + str(self.callcounter) + " made at " + str(time.time()) + " raised exception: " + str(huggingface_exception) + ". We will re-try the call.\n")
                
            # Add our failed attempt to the price calculation. NOTE: We add it as a single call only, as a proper token-calculation cannot be done
            # when completion-tokens are unknown and only tiktoken-estimates are available for prompt-tokens:
            self.api_totalprice = self.api_totalprice + self.Costs_price
                
        # If no exception was made, we can safely continue. Otherwise, we must simply state that there was no success
        # and wait for the next iteration in the while-loop:
        if not huggingface_call_succeeded:
                
            # Then, we simply state that there is no success and stop doing anything until the next while-iteration:
            Response_IsOK = False
                
        else:
                
            # Next, we mus decide whether the obtained response suffices, so begin by declaring the boolian to be true:
            Response_IsOK = True

            # Log our data:
            if (verbose_option>=0):
                if isinstance(self.logfile, io.TextIOBase):
                    if self.logfile.writable():
                        self.logfile.write("Huggingface Call " + str(self.callcounter) + " made at " + str(time.time()))
                                
            # Calculate costs:
            self.api_totalprice = self.api_totalprice + self.Costs_price
                
        # Next, we can start to process the actual responce into a usable text-string.
        if Response_IsOK:

            # Then, transform the output of Huggingface back into a string:
            short_responce = self.huggingface_tokenizer.decode(summary_ids[0],skip_special_tokens=True)

            # Then, remove capped text:
            short_responce = get_complete_sentences(short_responce)
            
            # Check the length of the response. It should not be too short: we want at least 0.4* of the max. summary length,
            # unless the text we summarize is shorter. Then we want at least 0.4* that length. This is crucial, as otherwise
            # some texts may never succeed.
            length_summary = len(short_responce.split())
                
            if (length_summary<0.3*min(self.MaxSummaryLength,length_textpiece)):

                # Then, the returned summary is too short:
                Response_IsOK = False
                
                if (verbose_option>=0):
                    print("Huggingface returned a summary that is way too short. len(summary)="+str(length_summary)+" and len(text)=" + str(length_textpiece))
                        
                    if (verbose_option>0):
                        print(" ==> textpiece: ==> ")
                        print(textpiece)
                        print("")
                        print(" ==> Summary: ==> ")
                        print(short_responce)
                        print("")
                    
                # Log our data:
                if (verbose_option>=0):
                    if isinstance(self.logfile, io.TextIOBase):
                        if self.logfile.writable():
                            self.logfile.write("Huggingface Call " + str(self.callcounter) + " returned a summary that was too short. We will re-try the call.\n")
                
        # So, if at this point the response suffices, then we have that Response_IsOK==True and we move on to the next item in the summarize-array.
            
    # -----------------------------------------------------------------------
    # Next, end the while-loop & exception-test and keep the response from Huggingface that we like:
    TheSummary = short_responce
    
    # Give some output (verbosity):
    if (verbose_option>1):
        print("textsplitter.summarize() is under development")
        print("Number of words = " + str(len(textpiece_nobreaks)))
        print("\n")
        print("[TEXT]")
        print("\n")
        print(textpiece_nobreaks)
        print("\n")
        print("[SUMMARY]")
        print(TheSummary)

    # Then, we can now return the answer:
    return TheSummary
