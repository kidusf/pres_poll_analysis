#Presidential Polls Dataset and Analysis for the 2020 General Election
#Made by: Kidus Fasil
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


#reading the data
polls=pd.read_csv('president_polls_historical.csv')
num_states=51
#converting dates to date times
polls["end_date"]=pd.to_datetime(polls["end_date"])
#cleaning and subsetting data
state_polls=polls[["poll_id","state","end_date", "answer", "candidate_party", "pct"]].fillna("Unknown")
#filtered the data to when Bernie Sanders dropped out of the race
filtered_date=pd.to_datetime("2020-04-09")
state_polls=state_polls[state_polls["end_date"]>filtered_date]
national_polls=polls[["poll_id","end_date", "answer", "candidate_party", "pct"]].fillna("Unknown")
national_polls=national_polls[national_polls["end_date"]>filtered_date]
#hardcoded the state names of the US and electoral votes per state
#Using a dictionary for predict()
state_names={"Alabama":9, "Alaska":3, "Arizona":11,"Arkansas":6, "California":55, "Colorado":9, "Conneticut":7, "Delaware":3, "District of Columbia":3, "Florida":29, "Georgia":16, "Hawaii":4, "Idaho":4, "Illinois":20, "Indiana":11, "Iowa":6, "Kansas":6, "Kentucky":8, "Louisiana":8, "Maine":4, "Maryland":10, "Massachusetts":11, "Michigan":16, "Minnesota":10, "Mississippi":6, "Missouri":10, "Montana":3, "Nebraska":5, "Nevada":6, "New Hampshire":4, "New Jersey":14, "New Mexico":5, "New York":29, "North Carolina":15, "North Dakota":3, "Ohio":18, "Oklahoma":7, "Oregon":7, "Pennsylvania":20, "Rhode Island":4, "South Carolina":9, "South Dakota":3, "Tennesee":11, "Texas":38, "Utah":6, "Vermont":3, "Virginia":13, "Washington":12, "West Virginia":5, "Wisconsin":10, "Wyoming":3}
state_list_data=[]
state_keys=list(state_names.keys())
#creating a list of tables for each state
for i in range(num_states):
    state_list_data.append(state_polls[state_polls["state"]==state_keys[i]])
#creates an empty dataframe for both leading candidates and takens in the data from all states
biden_data=pd.DataFrame()
trump_data=pd.DataFrame()
for i in range(num_states):
    biden_ans=state_list_data[i][state_list_data[i]["answer"]=="Biden"]
    trump_ans=state_list_data[i][state_list_data[i]["answer"]=="Trump"]
    biden_data.insert(i, state_keys[i], [biden_ans["pct"].mean()], True)
    trump_data.insert(i, state_keys[i], [trump_ans["pct"].mean()], True)
#cleans the data because there are some NaN values
biden_data.fillna(0)
trump_data.fillna(0)
poll_diff=biden_data-trump_data
#if the margin is negative, Trump is leading; if the margin is positive, Biden is leading
trump_lead=poll_diff[poll_diff.iloc[[0]]<0]
biden_lead=poll_diff[poll_diff.iloc[[0]]>0]
#predicts who will win based off electoral votes and polling data
def predict():
    biden_sum=0
    trump_sum=0
    for i in range(num_states):
        if(state_keys[i] in biden_lead.dropna(axis=1)):
            biden_sum+=state_names[state_keys[i]]
        if(state_keys[i] in trump_lead.dropna(axis=1)):
            trump_sum+=state_names[state_keys[i]]
    #makes the bar graph have a blue bar for Biden and red graph for Trump
    color=["blue" if (y==biden_sum) else "red" for y in [biden_sum, trump_sum]]
    #using seaborn to plot the results
    plt.ylabel("Electoral Votes")
    plt.xlabel("Candidate")
    sb.barplot(x=["Biden", "Trump"], y=[biden_sum, trump_sum], palette=color)
    if(biden_sum>trump_sum):
        plt.title("Biden wins: "+str(biden_sum)+"-"+str(trump_sum))
    elif(trump_sum>biden_sum):
        plt.title("Trump wins: "+str(trump_sum)+"-"+str(biden_sum))
    else:
        plt.title("It's a tie: "+str(trump_sum)+"-"+str(biden_sum))
    plt.show()

def plotData(state_idx):
    #plotting a trendline for poll numbers throughout the election year for the frontrunning candidates for each state
    biden_data_by_date=[]
    trump_data_by_date=[]
    jorgensen_data_by_date=[]
    hawkins_data_by_date=[]
    data_by_date=[]
    #the data set is already sorted by date so the first date is 11/3/2020
    min_date=polls["end_date"][0]
    unique_date=True
    #itr_data is the data set that will be iterated through depending on state or national data
    itr_data=None
    #if national use national data set, else use state data set
    if(state_idx==52):
        itr_data=national_polls
    else:
        itr_data=state_list_data[state_idx]
    for dates in itr_data["end_date"]:
        #collecting all of the polls that said Biden/Trump/Jorgensen/Hawkins on the same date and averaging the data
        if(dates==min_date):
            biden_data=itr_data[(itr_data["end_date"]==min_date) & (itr_data["answer"]=="Biden")]
            trump_data=itr_data[(itr_data["end_date"]==min_date) & (itr_data["answer"]=="Trump")]
            jorgensen_data=itr_data[(itr_data["end_date"]==min_date) & (itr_data["answer"]=="Jorgensen")]
            hawkins_data=itr_data[(itr_data["end_date"]==min_date) & (itr_data["answer"]=="Hawkins")]
            #checks if the date is unique so it can average that date's poll numbers
            if(unique_date):
                biden_points=biden_data["pct"].mean()
                trump_points=trump_data["pct"].mean()
                jorgensen_points=jorgensen_data["pct"].mean()
                hawkins_points=hawkins_data["pct"].mean()
                biden_data_by_date.append(biden_points)
                trump_data_by_date.append(trump_points)
                jorgensen_data_by_date.append(jorgensen_points)
                hawkins_data_by_date.append(hawkins_points)
                data_by_date.append(min_date)
                unique_date=False
        #if the date is lower than min date, then move on to the next date
        if(dates<min_date):
            min_date=dates
            unique_date=True
    #plotting the data
    plt.plot(np.array(data_by_date), np.array(biden_data_by_date), marker="o", color="b")
    plt.plot(np.array(data_by_date), np.array(trump_data_by_date), marker="o", color="r")
    plt.plot(np.array(data_by_date), np.array(jorgensen_data_by_date), marker="o", color="y")
    plt.plot(np.array(data_by_date), np.array(hawkins_data_by_date), marker="o", color="g")
    plt.xlabel("Date")
    plt.ylabel("Percentage of the Vote")
    plt.legend(["Biden", "Trump", "Jorgensen", "Hawkins"])
    if(state_idx==52):
        plt.title("National")
    else:
        plt.title(state_keys[state_idx])
    plt.show()
    #showing summary statistics of the state's polling data
    biden_dataset=pd.DataFrame(np.array(biden_data_by_date))
    trump_dataset=pd.DataFrame(np.array(trump_data_by_date))
    jorgensen_dataset=pd.DataFrame(np.array(jorgensen_data_by_date))
    hawkins_dataset=pd.DataFrame(np.array(hawkins_data_by_date))
    print("____________________________________"+"\n")
    print("Biden: "+"\n")
    print(biden_dataset.describe())
    print()
    print("Trump: "+"\n")
    print(trump_dataset.describe())
    print()
    print("Jorgensen: "+"\n")
    print(jorgensen_dataset.describe())
    print()
    print("Hawkins: "+"\n")
    print(hawkins_dataset.describe())
    print()
    print("____________________________________"+"\n")
    
def statesByMargin():
    #poll_diff takes the difference between the biden % and trump %
    #margins defined by tilt(<1%), lean(1%<=p<5%), likely(5%<=p<15%), and safe(p>=15%)
    tilt_states=poll_diff[abs(poll_diff.iloc[[0]])<1.0].dropna(axis=1)
    lean_states=poll_diff[(abs(poll_diff.iloc[[0]])<5.0) & (abs(poll_diff.iloc[[0]])>=1.0)].dropna(axis=1)
    likely_states=poll_diff[(abs(poll_diff.iloc[[0]])<15.0) & (abs(poll_diff.iloc[[0]])>=5.0)].dropna(axis=1)
    safe_states=poll_diff[abs(poll_diff.iloc[[0]])>=15.0].dropna(axis=1)
    #using seaborn to plot the margins
    sb.barplot(data=biden_lead,  color="b")
    sb.barplot(data=trump_lead,  color="r")
    plt.legend(["Biden Lead", "Trump Lead"])
    plt.title("State Margins")
    plt.xlabel("State")
    plt.ylabel("Margin")
    plt.show()
    print("------------------------------------------------------------------------------"+"\n")
    print("Negative numbers mean Trump is leading, positive numbers mean Biden is leading"+"\n")
    print("Tilt States"+"\n")
    print(tilt_states)
    print()
    print("Lean States"+"\n")
    print(lean_states)
    print()
    print("Likely States"+"\n")
    print(likely_states)
    print()
    print("Safe States"+"\n")
    print(safe_states)
    print()
    print("------------------------------------------------------------------------------"+"\n")


while(True):
    #sample output
    title="Presiential Polling Analysis"
    print(title+"\n")
    print("_"*len(title)+"\n")
    print("Options"+"\n")
    print("1. View a states polling data"+"\n")
    print("2. View national polls"+"\n")
    print("3. View state margins"+"\n")
    print("4. Predict who will win"+"\n")
    print("5. Quit"+"\n")
    print("_"*len(title))
    option=int(input("Select an option: "))
    if(option==1):
        state_selected=input("Enter a state to view its polling data: ")
        state_idx=state_keys.index(state_selected)
        if(state_idx==-1):
            print("Not a valid state")
        else:
            plotData(state_idx)
    elif(option==2):
        state_idx=52
        plotData(state_idx)
    elif(option==3):
        statesByMargin()
    elif(option==4):
        predict()
    elif(option==5):
        yn=input("Are you sure you want to quit?(Yes/No): ")
        if(yn=="Yes"):
            print("Quitting..."+"\n")
            break
        elif(yn=="No"):
            continue
        else:
            print("not a valid input")
    else:
        print("Not a valid input")
#END OF PROGRAM


    


    

