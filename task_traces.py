import utils
import llms
import os


def query_gpt(folder="prompt_patterns_traces", reps=10):
    prompts = utils.get_files_in_folder(folder)

    # LOOP THROUGH EACH PROMPT FILE
    for prompt in prompts:
        promptfilename = prompt
        prompt = utils.read_file(prompt)

        # ITERATE THROUGH TWO REQUIREMENTS SPECIFICATIONS
        for folder in ["data/1998_themas_clean", "data/2003_qheadache_clean"]:
            with open(folder + ".txt", "r") as specification:
                specification = specification.read()
                for file_name in os.listdir(folder):
                    file = utils.read_file_contents(folder + "/" + file_name)

                    # COPY THE PROMPT AND REPLACE "[DEPRECATED]" WITH THE CONTENT OF THE FIRST LINE OF THE FILE
                    tempprompt = prompt
                    tempprompt = tempprompt.replace("[deprecated]", file[0])
                    tempprompt = tempprompt + "\n" + specification

                    replypath = "replies_traces/" + promptfilename.split("/")[1][:-4] + "/"
                    if not os.path.exists(replypath):
                        os.mkdir(replypath)

                    # GENERATE REPLIES MULTIPLE TIMES (CONTROLLED BY 'REPS') AND SAVE THEM
                    for _ in range(reps):
                        reply = llms.gpt3_prompt(tempprompt, engine="gpt-3.5-turbo", temperature=0.4)
                        utils.write_text_file(promptfilename + " " + folder + " " + file_name + "\n\n" + reply, path=replypath)


if __name__ == '__main__':
    llms.init_openai()
    query_gpt("prompt_patterns_traces", reps=3)
