# Initialize an empty set
result_set = set()

# Get user input
try:
    user_input = float(input("Enter persons body temperature:(in Fahreneit)"))
    
    # Check the input range and add corresponding values to the set
    if 103 < user_input <= 107.5:
        result_set.update(["Bronchitis", "COPD" , "Pneumonia" , "Laryngomalacia" , "Cystic Fibrosis"])
    elif 101.1 < user_input <= 103:
        result_set.update(["Bronchitis", "COPD" , "Pneumonia" , "Epiglottitis" , "Laryngomalacia" , "Cystic Fibrosis"])
    elif 101 < user_input <= 101.1:
        result_set.update(["Bronchitis", "COPD" , "Pneumonia" , "Epiglottitis" , "Laryngomalacia"])
    elif 100.4 < user_input <= 101:
        result_set.update(["Bronchitis", "COPD" , "Pneumonia" , "Laryngomalacia"])
    elif 99.6 < user_input <= 100.4:
        result_set.update(["Bronchitis", "COPD"])
    elif 99.4 < user_input <= 99.6:
        result_set.update(["COPD"])
    elif 97.4 < user_input <= 99.4:
        print("Our Patient seems quite healthy")
    elif 93 < user_input <= 97.4:
        result_set.update(["Heart Disease"])
    else:
        print("Make sure that the person is breathing.")
except ValueError:
    print("Invalid input. Please enter a number as temperature.")

# Print the resulting set
print("Resulting Vulnerability set:", result_set)
