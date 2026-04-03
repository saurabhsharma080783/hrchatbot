import os
import boto3
import streamlit as st
import uuid
# This tells the app to use keys from Azure settings

# --- 1. AWS CONFIGURATION ---
# Fill these with your details from the AWS Console
AGENT_ID = 'abc' 
AGENT_ALIAS_ID = 'aaa' 
REGION = 'us-east-1' # e.g., us-east-1


client = boto3.client(
    "bedrock-agent-runtime",
    aws_access_key_id=os.getenv("AKIAUOF72WOIMGUTABEL"),
    aws_secret_access_key=os.getenv("KvaLxr/zV1XWSXE02BCdrs4TsHt8FIpfHOkCVNXY"),
    region_name="us-east-1"
)



# Initialize the Bedrock client
client = boto3.client("bedrock-agent-runtime", region_name=REGION)

# --- 2. USER INTERFACE SETUP ---
st.set_page_config(page_title="Company HR Assistant", page_icon="🏢")
st.title("🏢 HR Policy Assistant")
st.markdown("Ask me about leave policies, travel, onboarding, or benefits.")

# Initialize chat history so it remembers the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4()) # Unique ID for this chat session

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. HANDLING USER INPUT ---
if prompt := st.chat_input("How many days of casual leave do I have?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call AWS Bedrock Agent
    with st.chat_message("assistant"):
        try:
            response = client.invoke_agent(
                agentId=AGENT_ID,
                agentAliasId=AGENT_ALIAS_ID,
                sessionId=st.session_state.session_id,
                inputText=prompt,
            )
            
            # Extract the text from the response
            event_stream = response['completion']
            full_response = ""
            for event in event_stream:
                if 'chunk' in event:
                    data = event['chunk']['bytes'].decode("utf-8")
                    full_response += data
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
