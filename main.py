from queries import find_by_author, find_by_tag
import connect

message = """
Enter your query in the following format:
    name: <author>
    tag: <tag>
    tags: <tag1,tag2,tag3>
if you want to exit, enter "exit"
if you need help, enter "help"
"""


def process_query(query: str):
    if query == "help":
        return message

    query_error = "[Error]", "Wrong query, try again"
    try:
        key, value = query.split(":")
        if key not in ["name", "tag", "tags"]:
            return query_error

        if key == "name":
            return find_by_author(value.strip())

        elif key == "tag":
            try:
                res = find_by_tag(value.strip())[0]

                return res[0], res[1]

            except IndexError:
                return query_error

        elif key == "tags":
            if "," not in value:
                return find_by_tag(value.strip())[0]
            tags = [tag.strip() for tag in value.split(",")]
            return [find_by_tag(tag)[0] for tag in tags]
        else:
            return query_error
    except ValueError:
        return query_error


def print_result(result):
    try:
        quotes, author = result
        if isinstance(quotes, list):
            for item in quotes:
                print(f"{item} - {author}")
                print("------------------------")
        elif isinstance(quotes, str):
            print(f"{quotes} - {author}")
            print("------------------------")

        elif isinstance(result, list):
            for item in set(result):
                print(f"{item[0]} - {item[1]}")
                print("------------------------")
        else:
            print("Invalid result")
    except TypeError:
        print("Invalid result")


if __name__ == "__main__":
    print(message)
    while True:
        query = input(">>>")
        if query == "exit":
            print("Bye!")
            break

        print_result(process_query(query))
