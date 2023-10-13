import fw_reponses.hbi_responses_tests as responses_tests
import fw_reponses.hbi_responses_stage as responses_stage


RESPONSE_MESSAGE_CODE = 6

RESPONSE_MAPPING = {}
RESPONSE_MAPPING.update(responses_tests.RESPONSE_TEST_MAPPING) #add the handler for the test message responses
RESPONSE_MAPPING.update(responses_stage.RESPONSE_STAGE_MAPPING) #add the handler for the power stage message responses

def handle_response(byte_stream):
    if(byte_stream[3] in RESPONSE_MAPPING):
        print("Received response message (code {code}) ...  Redirecting to appropriate handler".format(code = byte_stream[3]))
        payload_length = byte_stream[2] #grab the length of the payload
        RESPONSE_MAPPING[byte_stream[3]](byte_stream[4:4+payload_length-1]) #pass along the message payload (aside from the response code) to the appropriate handler
    else:
        print("Received unknown response message (code {code})".format(code = byte_stream[3]))