import utils
import llms
import os
import random


def query_gpt(folder="prompt_patterns_traces", reps=10):
    database = utils.load_csv_file("data/nfr.csv")
    prompts = utils.get_files_in_folder(folder)

    counter = 0
    for elem in database:
        elem["ID"] = counter
        counter += 1

    # FOR EACH TEMPERATURE SETTING (IN THE PAPER)
    for temperature in [0, 0.4, 1]:
        # A NUMBER OF TIMES (10, IN THE PAPER)
        for _ in range(reps):
            for prompt in prompts:
                promptfilename = prompt
                prompt = utils.read_file(prompt)

                # GENERATE SAMPLES
                sample = ""
                gold = ""

                # RANDOMLY SAMPLE REQUIREMENTS FROM DATASET TO INCLUDE IN PROMPT
                for reqid in range(5):
                    elem = random.choice(database)
                    sample += "(ID="+str(elem["ID"])+") " + elem["Requirement"] + "\n"
                    gold += str(elem["ID"]) + "," + elem["Type"]+"\n"

                # ADD SAMPLED REQUIREMENTS TO PROMPT
                tempprompt = prompt
                tempprompt = tempprompt + "\n" + sample

                replypath = "replies_classify/" + promptfilename.split("/")[1][:-4] + "/"
                if not os.path.exists(replypath):
                    os.mkdir(replypath)

                # ASK COMPLETION AND WRITE FILES
                reply = llms.gpt3_prompt(tempprompt, engine="gpt-3.5-turbo", temperature=temperature)
                utils.write_text_file(promptfilename + "\n\nPROMPT:\n" + tempprompt + "\n\nGOLD:\n" + gold + "\n\nREPLY:\n" + reply, path=replypath)


if __name__ == '__main__':
    llms.init_openai()
    query_gpt("prompt_patterns_classify", reps=50)
