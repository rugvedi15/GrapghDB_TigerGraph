import pyTigerGraph as tg
import json
import pandas as pd

hostname = "https://5c97db8ab1d345a499a689ead868baa6.i.tgcloud.io"
graphName = "clinical_graph"
secret = "oa42tb3jfp6ntubbr7qlnt34gccsfprn"
username = "rugvedi"
password = "Clinical@1"

# graphtemp = tg.TigerGraphConnection(host=hostname, graphname=graphName)

graph = tg.TigerGraphConnection(host=hostname, graphname=graphName, username=username, password=password,
                                gsqlSecret=secret)
authToken = graph.getToken(secret)
authToken = authToken[0]

schema = graph.getSchema()
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# print(json.dumps(schema, indent=2))

# print("Vertex Types")
# print(graph.getVertexTypes())
# print("Vertex Types for Patients")
# print(graph.getVertexType("patients"))
# print("Vertex Count")
# print(graph.getVertexCount("*"))
# print("Edge Types")
# print(graph.getEdgeTypes())
# print("Edge Count")
# print(graph.getEdgeCount())
# print(json.dumps(graph.getVertices("patients"), indent=2))
print(json.dumps(graph.getVertexStats("patients"), indent=2))
print(graph.gsql('ls'))
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
graph.gsql('USE GRAPH clinical_graph')
result = graph.gsql('SHOW JOB *')
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_________________________
# result = graph.gsql("""
#                     USE GRAPH clinical_graph
#                     CREATE QUERY testQuery() FOR GRAPH clinical_graph {
#                     PRINT "testQuery work!";
#                     }
#                     """
#                 )
# print(result)

# result = graph.gsql("""
#                     USE GRAPH clinical_graph
#                     INTERPRET QUERY testQuery()
#                     """)
# print(result)
# _____________________WORKING_ENDS_________________________

# _____________________WORKING_________________________
result = graph.runInterpretedQuery("""
        INTERPRET QUERY testQuery1() FOR GRAPH clinical_graph {
                                   PRINT "Test Query 1 Works!";
        }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________

# _____________________WORKING_________________________
# average heathcare_expenses
result = graph.runInterpretedQuery("""
        INTERPRET QUERY avg_hc() FOR GRAPH clinical_graph {
            AvgAccum @@avg_healthcost;

            graph_set = {patients.*};

            patients_data = SELECT p FROM graph_set:p
                            ACCUM
                                @@avg_healthcost += p.heathcare_expenses;
            PRINT @@avg_healthcost;
        }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________


# _____________________WORKING_________________________
# general highest expense fron patient
result = graph.runInterpretedQuery("""
    INTERPRET QUERY max_healthcare_cost() FOR GRAPH clinical_graph {
        MaxAccum<FLOAT> @@max_healthcost;

        graph_set = {patients.*};

        patients_data = SELECT p FROM graph_set:p
                        ACCUM
                            @@max_healthcost += (p.heathcare_expenses - p.healthcare_coverage);
        max_expense_patient_data = SELECT p from graph_set:p 
                                    where abs(((p.heathcare_expenses - p.healthcare_coverage)) - (@@max_healthcost)) < 0.000000001;
        PRINT @@max_healthcost;
        PRINT max_expense_patient_data;
    }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________

# _____________________WORKING_________________________
# city wise highest expense from patient
result = graph.runInterpretedQuery("""
    INTERPRET QUERY max_city_healthcare_cost(STRING city = "Franklin") FOR GRAPH clinical_graph {
        MaxAccum<FLOAT> @@city_max_healthcost;

        graph_set = {patients.*};

        patients_data = SELECT p FROM graph_set:p where UPPER(p.city) == UPPER(city)
                        ACCUM
                            @@city_max_healthcost += (p.heathcare_expenses - p.healthcare_coverage);
        max_expense_patient_data = SELECT p from graph_set:p 
                                    where abs(((p.heathcare_expenses - p.healthcare_coverage)) - (@@city_max_healthcost)) < 0.000000001;
        PRINT @@city_max_healthcost;
        PRINT max_expense_patient_data;
    }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________


# _____________________WORKING_________________________
# country wise highest expense from patient
result = graph.runInterpretedQuery("""
    INTERPRET QUERY max_country_healthcare_cost(STRING country="Essex County") FOR GRAPH clinical_graph {
        MaxAccum<FLOAT> @@country_max_healthcost;

        graph_set = {patients.*};

        patients_data = SELECT p FROM graph_set:p where UPPER(p.country) == UPPER(country)
                        ACCUM
                            @@country_max_healthcost += (p.heathcare_expenses - p.healthcare_coverage);
        max_expense_patient_data = SELECT p from graph_set:p 
                                    where abs(((p.heathcare_expenses - p.healthcare_coverage)) - (@@country_max_healthcost)) < 0.000000001;
        PRINT @@country_max_healthcost;
        PRINT max_expense_patient_data;
    }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________


# _____________________WORKING_________________________
# city wise highest expense from patient
result = graph.runInterpretedQuery("""
    INTERPRET QUERY max_state_healthcare_cost(STRING state="Massachusetts") FOR GRAPH clinical_graph {
        MaxAccum<FLOAT> @@state_max_healthcost;

        graph_set = {patients.*};

        patients_data = SELECT p FROM graph_set:p where UPPER(p.state) == UPPER(state)
                        ACCUM
                            @@state_max_healthcost += (p.heathcare_expenses - p.healthcare_coverage);
        max_expense_patient_data = SELECT p from graph_set:p 
                                    where abs(((p.heathcare_expenses - p.healthcare_coverage)) - (@@state_max_healthcost)) < 0.000000001;
        PRINT @@state_max_healthcost;
        PRINT max_expense_patient_data;
    }
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________

# _____________________WORKING_________________________
# number of patients and records of patients paying more than threshold or average heathcare_expenses
result = graph.runInterpretedQuery("""
        INTERPRET QUERY avg_threshold_healthcost(FLOAT threshold = 1500000) FOR GRAPH clinical_graph { 
   AvgAccum @@avg_healthcost;

   graph_set = {patients.*};

   patients_data = SELECT p FROM graph_set:p
                    ACCUM
                      @@avg_healthcost += p.heathcare_expenses;
   FLOAT effective_threshold;

   IF threshold > 0.0
   THEN
      effective_threshold = threshold;
   ELSE
      effective_threshold = abs(@@avg_healthcost);
   END;                

    SumAccum<INT> @@patient_paying_above_threshold_count;                
   above_threshold_patients = SELECT p from graph_set:p where (((p.heathcare_expenses - p.healthcare_coverage)) - (effective_threshold)) > 0
                                ACCUM @@patient_paying_above_threshold_count += 1;
   PRINT "Threshold Value: " + to_string(threshold);
   PRINT "Number of patients paying above threshold: " + to_string(@@patient_paying_above_threshold_count);
   PRINT above_threshold_patients;
}
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________

# _____________________WORKING_________________________
# most prominent condition patients face in world
result = graph.runInterpretedQuery("""
        INTERPRET QUERY most_common_condition() FOR GRAPH clinical_graph {
    SumAccum<INT> @@condition_count_total;
    MapAccum<STRING, INT> @@condition_count;

    # Traverse and count occurrences of each condition_code
    result = SELECT c
             FROM patients:p - (conditions_patients:e) - conditions:c
             ACCUM @@condition_count += (c.condition_code -> 1)
             POST-ACCUM @@condition_count_total += 1;

    # Print the total count of all conditions
    PRINT @@condition_count_total;

    # Initialize variables for finding the maximum
    STRING max_condition_code = "";
    INT max_count = 0;

    # Iterate over map entries to find the condition_code with the highest count
    FOREACH (key,value) IN @@condition_count DO
        IF value > max_count THEN
            max_count = value;
            max_condition_code = key;
        END;
    END;

    # Print the most common condition_code and its count
    PRINT "Most Common Condition Code: " + max_condition_code + ", Count: " + to_string(max_count);
  result = SELECT c from conditions:c where c.condition_code == max_condition_code;
  print result;
}
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________


# _____________________WORKING_________________________
# most prominent conditions faced by patients in a specific city
result = graph.runInterpretedQuery("""
        INTERPRET QUERY city_most_common_condition(STRING city = "Chatham") FOR GRAPH clinical_graph {
    SumAccum<INT> @@city_condition_count_total;
    MapAccum<STRING, INT> @@condition_count;

    # Traverse and count occurrences of each condition_code
    result = SELECT c
             FROM patients:p - (conditions_patients:e) - conditions:c
             WHERE Upper(p.city) == Upper(city)
             ACCUM @@condition_count += (c.condition_code -> 1)
             POST-ACCUM @@city_condition_count_total += 1;

    # Print the total count of all conditions
    PRINT @@city_condition_count_total;

    # Initialize variables for finding the maximum
    STRING max_condition_code = "";
    INT max_count = 0;

    # Iterate over map entries to find the condition_code with the highest count
    FOREACH (key,value) IN @@condition_count DO
        IF value > max_count THEN
            max_count = value;
            max_condition_code = key;
        END;
    END;

    # Print the most common condition_code and its count
    PRINT "Most Common Condition Code in " + city + " city: " + max_condition_code + ", Count: " + to_string(max_count);
  result = SELECT c from conditions:c where c.condition_code == max_condition_code;
  print result;
}
""")
print(result)
print("-------------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------------")
# _____________________WORKING_ENDS_________________________


# query2 = """
# CREATE QUERY q5_max_expenses() FOR GRAPH clinical_graph SYNTAX v2 {
#     SetAccum<STRING> @@sorted_patients;
#     SetAccum<FLOAT> @@sorted_expenditures;

#     Seed = {patients.*};

#     SortedPatientData =
#         SELECT s
#         FROM Seed:s
#         ORDER BY s.healthcare_expenses DESC
#         LIMIT 1;

#     top_patient =
#         SELECT s
#         FROM SortedPatientData:s
#         ACCUM
#             @@sorted_patients += s.id,
#             @@sorted_expenditures += s.healthcare_expenses;

#     PRINT @@sorted_patients;
#     PRINT @@sorted_expenditures;
# }
# """

# # Install the query
# try:
#     graph.gsql(query2)
#     print("Query installed successfully.")
# except Exception as e:
#     print(f"Error installing query: {e}")

# try:
#     response2 = graph.runInstalledQuery("q5_max_expenses")
#     print("Query executed successfully.")
#     # Display the results
#     for patient in response2[0]["@@sorted_patients"]:
#         print(f"Patient ID: {patient}")

#     for expenditure in response2[0]["@@sorted_expenditures"]:
#         print(f"Healthcare Expenditure: {expenditure}")
# except Exception as e:
#     print(f"Error running query: {e}")

# # /restpp/query/clinical_graph/q4_PatientId_to_allergy?id=<STRING>