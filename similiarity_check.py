import textdistance
import pandas as pd

def similar(a, b):
    similarity = 1-textdistance.Cosine(qval=2).distance(a, b)     
    return similarity *100

    SAP1 = pd.read_csv('sap_eng.csv')
SAP1 = SAP1[SAP1.description.notnull()]

print(SAP1)
SAP2 = pd.read_csv('sap_eng.csv') 
SAP2 = SAP2[SAP2.description.notnull()]

scores = pd.DataFrame({'SAP1': SAP1['description']}, columns = ['SAP1', 'SAP2', 'Similarity']) 

# Temporary variable to store both the highest similarity score, and the 'SAP2' value the score was computed with
highest_score = {"score": 0, "description": ""}

# Iterate though SAP1['Description']
for job in SAP1['description']:
  highest_score = {"score": 0, "description": ""} # Reset highest_score at each iteration
  for description in SAP2['description']: # Iterate through SAP2['Description']
    similarity_score = similar(job, description) # Get their similarity

    if(similarity_score > highest_score['score']): # Check if the similarity is higher than the already saved similarity. 
#If so, update highest_score with the new values
      highest_score['score'] = similarity_score
      highest_score['description'] = description
    if(similarity_score == 100): # If it's a perfect match, don't bother continuing to search.
      break
  # Update the dataframe 'scores' with highest_score
  scores['SAP2'][scores['SAP1'] == job] = highest_score['description'] 
  scores['Similarity'][scores['SAP1'] == job] = highest_score['score']


  # Output it to Scores.csv without the index column (0, 1, 2, 3... far left in scores above). 
#Remove index=False if you want to keep the index column.
scores.to_csv('Scores.csv', index=False)