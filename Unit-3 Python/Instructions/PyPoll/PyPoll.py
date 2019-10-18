
#import os module to allow us to create file paths across operating systems
import os
#import module for reading csv files
import csv
    
def print_results():
    
    print("""Election Results
-----------------------------------------""")
    print(f"Total Votes: {int(len(VoterID))}")
    print("""----------------------------------------""")
    
    for candidate in Candidates:
        print(f'{candidate} : {"{:.3f}%".format(Vote_Percent[candidate])}  ({(Num_Votes[candidate])})')
    
    print("""----------------------------------------""")
    print(f"Winner: {Winner}")
    

#Assign path to open csvfile to read
input_file= os.path.join("Resources","election_data.csv") 
    
#define variables and lists to be used as per the analysis required

VoterID=[]        #stores all VoterID as list
County=[]       #stores County as list
Candidates=[]    #Stores Candidates as a list
Num_Votes={}     # dictionary for number of votes, keys as candidate and value as number of votes

#open the input file with the described path in csv format to read the data

with open(input_file,'r', newline="") as csvfile:
    
    #Read the input file as csv
    input_read= csv.reader(csvfile, delimiter=",")
    
    #dont need to read the headers
    next(csvfile, None)
    
    #looping to read every row and stores values as required
        
    for row in input_read:
        
        #store the VoterID as a list
        VoterID.append(row[0])
        
        candidate= row[2]
        
        if candidate not in Candidates:
        
            Candidates.append(candidate)        #unique list of candidates in election
            Num_Votes[candidate]=1              #counts the number of votes for a candidate
            
        else:
           Num_Votes[candidate]+=1              #counts the number of votes for a candidate
                       
    Total_Votes = len(VoterID) # total number of votes
    Vote_Percent= {candidate : (Num_Votes[candidate]/Total_Votes*100) \
                            for candidate in Candidates}        
    
    v=list(Vote_Percent.values())       #create list of values from dictionary
    k=list(Vote_Percent.keys())         #create list of keys from dictionary
    
    Winner= k[v.index(max(v))]          #return the index of max of values to get the corresponding winner
    
print_results()    

#prepare output list
output=[]
    
output.append("Election Results")
output.append("""------------------------------------""")
output.append(f"Total votes: {int(len(VoterID))}")
output.append("""------------------------------------""")

for candidate in Candidates:
    output.append(f'{candidate}: {"{:.3f}%".format(Vote_Percent[candidate])} ({Num_Votes[candidate]})' )

output.append("""------------------------------------""")
output.append(f"Winner: {Winner}")
    
    
#to export the results to a text file:
#define output path    

output_file= os.path.join("Resources","Election_data.txt")

#open the output file in write format
with open(output_file, 'w+') as text:
    
    #write lines from the output list
    for items in output:
        text.write(items +'\n')

    text.close()