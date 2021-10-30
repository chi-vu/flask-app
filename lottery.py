import requests
import sys
import bs4


def get_lottery_results():
    resp = requests.get("https://ketqua.net")
    tree = bs4.BeautifulSoup(resp.text, features="lxml")
    table = tree.find("table", attrs={"id": "result_tab_mb"}).find("tbody")
    awards = []
    for line in table.find_all("tr"):
        award = line.find_all("td")
        if len(award) > 1:
            for i in range(len(award)):
                awards.append(award[i].text)
    return awards


def print_lottery_results():
    awards = list(filter(lambda x: len(x) > 0, get_lottery_results()))
    index = list(
        map(
            lambda x: awards.index(x),
            list(filter(lambda x: x.isdigit() is not True, awards)),
        )
    )
    for i in range(len(index)):
        if i == len(index) - 1:
            numbers = awards[index[i] + 1:]
            print("{}: {}".format(awards[index[i]], ", "
                                  .join(map(str, numbers))))
        else:
            if index[i + 1] - index[i] == 2:
                numbers = awards[index[i] + 1]
                print("{}: {}".format(awards[index[i]], numbers))
            else:
                numbers = awards[index[i] + 1: index[i + 1]]
                print("{}: {}".format(awards[index[i]], ", "
                                      .join(map(str, numbers))))


def check_lottery_results(input_value):
    winning_numbers = list(
        map(
            lambda x: x[-2:],
            list(filter(lambda x: (x.isdigit() is True),
                        get_lottery_results()))
        )
    )
    for i in input_value:
        if i in winning_numbers:
            print("{}: HIT".format(i))
        else:
            print("{}: MISS".format(i))


def main():
    if len(sys.argv) < 2:
        print_lottery_results()
        sys.exit(1)

    input_value = sys.argv[1:]
    if any(i.isdigit() is not True or len(i) != 2 for i in input_value):
        print("Please enter values with 2-digit format")
        sys.exit(1)
    check_lottery_results(input_value)


if __name__ == "__main__":
    main()
