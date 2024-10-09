import streamlit as st
import pandas as pd


st.title("Let's begin to generate a GDPR policy")



st.markdown("### Privacy Policy Uses")

genre = st.radio(
    "What will this Privacy Policy be used for?",
    ["Website", "Mobile Application", "Facebook Application"],
    index=None,
)

st.write("You selected:", genre)



st.markdown("### User Location")

genre2 = st.radio(
    "Do you have users in the United States?",
    ["Yes", "No"],
    index=None,
)

genre3 = st.radio(
    "Do you have users in the EU, UK, Switzerland, Iceland, Liechtenstein, or Norway?",
    ["Yes", "No"],
    index=None,
)

genre4 = st.radio(
    "Do you have users in Canada?",
    ["Yes", "No"],
    index=None,
)

st.markdown("### Personal Information Collected Directly")
st.markdown("Please select the personal information you intend to collect directly from the user:")

table = ["Names","Phone numbers","Email addresses","Mailing addresses","Job titles",
         "Usernames","Passwords","Contact preferences","Contact or authentication data",
         "Billing addresses","Debit/credit card numbers"         
         ]
for i in table:
    st.checkbox(i)
# names = st.checkbox("Names")
# phone = st.checkbox("Phone numbers")
# names = st.checkbox("Email addresses")
# names = st.checkbox("Mailing addresses")
# names = st.checkbox("Job titles")
# names = st.checkbox("Usernames")
# names = st.checkbox("Usernames")



st.markdown("### Artifical Intellegence")

genre5 = st.radio(
    "Does your website or app offer AI-based services?",
    ["Yes", "No"],
    index=None,
)

if st.button("Submit to view the report"):
    st.write(f"Contact us for a free consultation https://calendly.com/clare_hsu/30min")

#     ## Order of passing the data into the pipeline:
#     cols=['person_age', 'person_income', 'person_home_ownership',
# 'person_emp_length', 'loan_intent', 'loan_grade', 'loan_amnt',
# 'loan_int_rate', 'loan_status', 'loan_percent_income',
# 'cb_person_default_on_file', 'cb_person_cred_hist_length']  ## List of columns of the original dataframe
        
#     input_data=[[age, income, house, emp, intent, grade, amt, interest, status, per_inc, per_def, hist]]

#     # pipe=joblib.load("model.pkl")  ## Loading the pipeline

#     input_data=pd.DataFrame(input_data,columns=cols)  ## Converting input into a dataframe with respective columns

#     # res=pipe.predict(input_data)[0]  ## Predicting the class
#     out={1:"The Customer is capable of DEFAULTING. Hence it is RISKY to provide loan!", 0:"The Customer is capable of NOT DEFAULTING. Hence it is POSSIBLE to provide loan!"}
#     # st.write(f"The Final Verdict obtained from the given model is that : {out[res]}")



# inputHouse_label = "Choose ownership type"
# #     bold_inputHouse_label = f"**{inputHouse_label}**"
# house = st.selectbox(inputHouse_label, [0, 1, 2, 3])

# inputLength_label = "Enter person's employment length:"
# #     bold_inputLength_label = f"**{inputLength_label}**"
# emp = st.number_input(inputLength_label)

# st.markdown("<b>Select the appropriate loan intent type: </b>", unsafe_allow_html=True)
# st.markdown("Debt consolidation --> 0")
# st.markdown("Education          --> 1")
# st.markdown("Home improvement   --> 2")
# st.markdown("Medical            --> 3")
# st.markdown("Personal           --> 4")
# st.markdown("Venture            --> 5")

# inputIntent_label = "Choose person's loan intent:"
# #     bold_inputIntent_label = f"**{inputIntent_label}**"
# intent = st.selectbox(inputIntent_label, [0,1,2,3,4,5])

# st.markdown("<b>Select the appropriate loan grade type: </b>", unsafe_allow_html=True)
# st.markdown("A --> 0")
# st.markdown("B --> 1")
# st.markdown("C --> 2")
# st.markdown("D --> 3")
# st.markdown("E --> 4")
# st.markdown("F --> 5")
# st.markdown("G --> 6")

# inputGrade_label = "Choose person's loan grade:"
# #     bold_inputGrade_label = f"**{inputGrade_label}**"
# grade = st.selectbox(inputGrade_label, [0,1,2,3,4,5,6])

# inputAmt_label = "Enter person's loan amount:"
# #     bold_inputAmt_label = f"**{inputAmt_label}**"
# amt = st.number_input(inputAmt_label)

# inputInterest_label = "Enter person's interest rate amount:"
# #     bold_inputInterest_label = f"**{inputInterest_label}**"
# interest = st.number_input(inputInterest_label)

# st.markdown("<b>Select the appropriate loan status type: </b>", unsafe_allow_html=True)
# st.markdown("Repaid --> 0")
# st.markdown("Pending --> 1")

# inputStatus_label = "Choose person's loan status:"
# #     bold_inputStatus_label = f"**{inputStatus_label}**"
# status = st.selectbox(inputStatus_label, [0,1], index=1)

# inputPerInc_label = "Enter person's loan percent income:"
# #     bold_inputPerInc_label = f"**{inputPerInc_label}**"
# per_inc = st.number_input(inputPerInc_label)

# st.markdown("<b>Select the appropriate type: </b>", unsafe_allow_html=True)
# st.markdown("No --> 0")
# st.markdown("Yes --> 1")

# inputPerDef_label = "Choose person's default:"
# #     bold_inputPerDef_label = f"**{inputPerDef_label}**"
# per_def = st.selectbox(inputPerDef_label, [0,1], index=1)

# inputHist_label = "Enter person's credit history length:"
# #     bold_inputHist_label = f"**{inputHist_label}**"
# hist = st.number_input(inputHist_label)

# if st.button("Predict Credit Score",key = 9)==1:
#     ## Order of passing the data into the pipeline:
#     cols=['person_age', 'person_income', 'person_home_ownership',
# 'person_emp_length', 'loan_intent', 'loan_grade', 'loan_amnt',
# 'loan_int_rate', 'loan_status', 'loan_percent_income',
# 'cb_person_default_on_file', 'cb_person_cred_hist_length']  ## List of columns of the original dataframe
        
#     input_data=[[age, income, house, emp, intent, grade, amt, interest, status, per_inc, per_def, hist]]

#     # pipe=joblib.load("model.pkl")  ## Loading the pipeline

#     input_data=pd.DataFrame(input_data,columns=cols)  ## Converting input into a dataframe with respective columns

#     # res=pipe.predict(input_data)[0]  ## Predicting the class
#     out={1:"The Customer is capable of DEFAULTING. Hence it is RISKY to provide loan!", 0:"The Customer is capable of NOT DEFAULTING. Hence it is POSSIBLE to provide loan!"}
#     # st.write(f"The Final Verdict obtained from the given model is that : {out[res]}")
