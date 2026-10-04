
print("===================================")
print("   Rule-Based Expert System")
print("   Student Health Advisory System")
print("===================================")

print("\nYou can answer in English, Spanish, Hindi, Gujarati, or Telugu.")
print("Examples:")
print("English: yes / no")
print("Spanish: si / sí / no")
print("Hindi: haan / हाँ / nahi / नहीं")
print("Gujarati: haa / હા / naa / ના")
print("Telugu: avunu / అవును / kaadu / కాదు")
print()


def get_answer(question):
    while True:
        answer = input(question).strip().lower()

        yes_answers = [
            "yes", "y",
            "si", "sí",
            "haan", "ha", "हाँ",
            "haa", "હા",
            "avunu", "అవును"
        ]

        no_answers = [
            "no", "n",
            "nahi", "नहीं",
            "naa", "ના",
            "kaadu", "కాదు"
        ]

        if answer in yes_answers:
            return "yes"

        elif answer in no_answers:
            return "no"

        else:
            print("Please enter yes/no in a supported language.")


fever = get_answer("Do you have fever? ")
cough = get_answer("Do you have cough? ")
sore_throat = get_answer("Do you have a sore throat? ")
headache = get_answer("Do you have a headache? ")
runny_nose = get_answer("Do you have a runny nose? ")
stomach_pain = get_answer("Do you have stomach pain? ")
vomiting = get_answer("Do you have vomiting? ")


def expert_system():

    # Rule 1
    if fever == "yes" and cough == "yes" and sore_throat == "yes":
        return "Possible respiratory infection. Consider getting medical advice."

    # Rule 2
    elif headache == "yes" and runny_nose == "yes" and sore_throat == "yes":
        return "Possible common cold. Get enough rest and stay hydrated."

    # Rule 3
    elif stomach_pain == "yes" and vomiting == "yes":
        return "Possible stomach-related illness. Stay hydrated and consider medical advice."

    # Rule 4
    elif headache == "yes" and fever == "yes":
        return "Fever with headache detected. Consider getting medical advice."

    # Rule 5
    elif cough == "yes":
        return "Cough detected. Get enough rest and monitor your symptoms."

    # Rule 6
    elif runny_nose == "yes":
        return "Runny nose detected. Rest and stay hydrated."

    # Rule 7
    elif sore_throat == "yes":
        return "Sore throat detected. Stay hydrated and get enough rest."

    # Rule 8 - No symptoms
    else:
        return "Congratulations big dog 🐐!! You don't have any symptoms. You are perfectly fine ❤️📈"


result = expert_system()

print("\n===================================")
print("Expert System Result:")
print(result)
print("===================================")