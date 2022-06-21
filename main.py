from queue import Queue
import string
import threading
import socket


def add_char(choice_word):
    list_add_char = [choice_word + c for c in string.ascii_lowercase]
    return list_add_char


def dot_subdomains(choice_word):
    list_dot_subdomains = []
    for i in range(1, len(choice_word)):
        if choice_word[i-1] != "-" and choice_word[i] != "-":
            list_dot_subdomains.append(choice_word[:i] + "." + choice_word[i:])
    return list_dot_subdomains


def del_char(choice_word):
    list_del_char = [choice_word[:i] + choice_word[i+1:] for i in range(len(choice_word))]
    return list_del_char


def homoglyphs(choice_word, i):
    list_homoglyphs = []

    if len(choice_word) == i:
        list_homoglyphs.append(choice_word)
        return

    letter = choice_word[i]
    if letter in dict_homoglyphs.keys():
        rep_word = choice_word[:i] + dict_homoglyphs[letter] + choice_word[i + 1:]
        homoglyphs(rep_word, i + 1)
        homoglyphs(choice_word, i + 1)
    else:
        homoglyphs(choice_word, i + 1)
    return list_homoglyphs


def create_list_all_words(choice_word):
    list_all_words = []

    for selected_word in choice_word:
        selected_word = selected_word.strip()

        list_all_words += add_char(selected_word)
        list_all_words += dot_subdomains(selected_word)
        list_all_words += del_char(selected_word)
        list_all_words += homoglyphs(selected_word, i=0)

    return list_all_words


def create_list_all_sites(list_all_words):
    all_sites = []
    for domain_zone in list_domain_zones:
        for domain_word in list_all_words:
            all_sites.append(domain_word + "." + domain_zone)
    return all_sites


def get_ip(q):
    while True:
        host = q.get()
        try:
            host_ip = socket.gethostbyname_ex(host)[2]
            list_ready_sites.append([host, host_ip])
        except socket.gaierror:
            pass

        q.task_done()


def main(list_all_sites):
    q = Queue()
    for _ in range(50):
        threading.Thread(target=get_ip, args=(q, ), daemon=True).start()

    for site in list_all_sites:
        q.put(site)

    q.join()


def format_ready_sites(ready_sites):
    for site, ips in ready_sites:
        if len(ips) > 1:
            message = ""
            for ip in ips:
                message += ip + "  "
            print(site, message)
        else:
            print(site, ips[0])


if __name__ == "__main__":
    list_domain_zones = [
        "com", "ru", "net", "org", "info", "cn", "es", "top", "au", "pl",
        "it", "uk", "tk", "ml", "ga", "cf", "us", "xyz", "top", "site",
        "win", "bid",
    ]
    dict_homoglyphs = {'o': '0', 'i': '1', 'l': '1'}
    word = list(input('Enter keywords (example "sberbank, google"): ').split(","))

    list_ready_sites = []
    main(create_list_all_sites(create_list_all_words(word)))
    format_ready_sites(list_ready_sites)


