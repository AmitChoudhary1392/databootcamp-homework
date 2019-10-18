
#import os module to allow us to create file paths across operating systems
import os
#import module for reading csv files
import csv

def print_analysis():
    
    print("""Financial Analysis
----------------------------------------------""")
    print(f"Total Months: {int(len(Dates))}")
    print(f"Total: ${Net_Total}")
    print(f"Average Change: $ {avgchange}")
    print(f"Greatest Increase in profit:{Dates[Change.index(GreatestInc)]} ( ${GreatestInc})")
    print(f"Greatest Decrease in profit:{Dates[Change.index(GreatestDec)]} ( ${GreatestDec})")


#Assign path to open csvfile to read
input_file= os.path.join("Resources","budget_data.csv") 
    
#define variables and lists to be used as per the analysis required

Dates=[]        #stores all dates as list
profit_loss=[]  #stores profit/loss values as list
Totalchange=0   #Total change value will hold the final change in profit and loss
Change=[]       #defines list to hold the change in profit/loss
GreatestInc=0   #variable to hold the greatest increase in profit
GreatestDec=0   #variable to hold the greatest decrease in profit
Net_Total=0     # variable to hold the net value of profit or loss
diff=[]         # holds values of change as a list to call the values as required

#open the input file with the described path in csv format to read the data

with open(input_file,'r', newline="") as csvfile:
    
    #Read the input file as csv
    input_read= csv.reader(csvfile, delimiter=",")
    
    #dont need to read the headers
    next(csvfile, None)
    
    #looping to read every row and stores values as required
    for row in input_read:
        
        #store the dates as a list
        Dates.append(row[0])
        
        # running total of the profit/loss values
        Net_Total+= float(row[1])
        
        #Create a list to hold profit/loss values
        profit_loss.append(row[1])
     
    # Calculate the change in profit/ loss value to determine max and min values
    for i in range(len(profit_loss)):
        
        if i==0:            #change should be of the same size as the other lists to recall corresponding values
            diff=0
                       
        else:
            diff=float(profit_loss[i])- float(profit_loss[i-1])    
            
        Totalchange+=diff
        Change.append(diff)   
        
    #Average change is total change divided by the actual no of changes i.e length of change list minus 1            
    avgchange= round((Totalchange/int(len(Change)-1)),2)    #rounding off to 2 decimal places  
    
    #calculate the greatest increase and decrease using the max and min fucntions
    GreatestInc=max(Change)
    GreatestDec= min(Change)
    
    #---------------------------------------------------------------------------------------------------------------
    #calculate the greatest increase and greatest decrease in profit/loss------
    #sort the list in descending order, using sort attribute, and printing the first and last index values
    #Change.sort(reverse=True)
    #GreatestInc= Change[0]
    #GreatestDec= Change[int(len(Change))-1]
    #----------------------------------------------------------------------------------------------------------------
    
    #call the print function to display the output
    print_analysis()

#to export the results to a text file:
#define output path    
output_file= os.path.join("Resources","budget_data.txt")

#open the output file in write format
with open(output_file, 'w+') as text:

    text.write("""Financial Analysis
----------------------------------------------""")
    text.write("\n" +"Total Months:" + str(int(len(Dates))) +"\n")
    text.write("Total: $" + str(Net_Total) +"\n")
    text.write("Average Change:" + " $" + str(avgchange) + "\n")
    text.write("Greatest Increase in profit: " + str(Dates[Change.index(GreatestInc)]) +" ($" + str(GreatestInc) +")" +"\n")
    text.write("Greatest Decrease in profit: " + str(Dates[Change.index(GreatestDec)]) +" ($" + str(GreatestDec) +")" +"\n")
    
    text.close()