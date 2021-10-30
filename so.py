import requests
import sys


def get_top_questions(n, label):
    params = {
        "pagessize": n,
        "tagged": label,
        "sort": "votes",
        "order": "desc",
        "site": "stackoverflow",
    }
    resp = requests.get("https://api.stackexchange.com/2.2/questions",
                        params=params)
    return resp.json()


def get_top_answer(n, label):
    question_resp = get_top_questions(n, label)
    try:
        for i in range(int(n)):
            question_id = question_resp.get("items")[i].get("question_id")
            params = {
                "pagesize": 1,
                "order": "desc",
                "sort": "votes",
                "site": "stackoverflow",
            }
            answer_resp = requests.get(
                "https://api.stackexchange.com/2.2/questions/{}/answers"
                .format(question_id), params=params,).json()
            title = question_resp.get("items")[i].get("title")
            answer_id = answer_resp.get("items")[0].get("answer_id")
            print("Title: {}".format(title))
            print("Link: https://stackoverflow.com/a/{}".format(answer_id))
    except IndexError:
        if not question_resp.get("items"):
            print("There is no questions with tag '{}'".format(label))


def main():
    if len(sys.argv) != 3:
        print("Please enter 2 values: [the number of questions] and [the tag]")
        sys.exit(1)
    n = sys.argv[1]
    label = sys.argv[2]
    if n.isdigit() is not True:
        print("The number of questions must be an integer")
        sys.exit(1)
    if int(n) == 0:
        print("The number of questions must be greater than 0")
        sys.exit(1)
    get_top_answer(n, label)


if __name__ == "__main__":
    main()
